"""Single-owner Marlin USB host. Never auto-reconnect or replay after a fault."""
import argparse
import functools
import hashlib
import json
import operator
import os
from pathlib import Path
import re
import signal
import sqlite3
import subprocess
import time

import serial

class Host:
    def __init__(self, root, connection):
        self.root, self.s = Path(root), connection
        self.root.joinpath('controls').mkdir(exist_ok=True)
        self.root.joinpath('control-results').mkdir(exist_ok=True)
        self.status = dict(pid=os.getpid(), state='connecting', acknowledged=0,
                           layer=0, speed_percent=100, file_line=0)
        self.number = 0
        self.stopping = False
        self.paused = False
        self.last_save = 0
        self.db = sqlite3.connect(self.root / 'progress.sqlite3')
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('CREATE TABLE IF NOT EXISTS checkpoint (id INTEGER PRIMARY KEY CHECK(id=1), data TEXT NOT NULL)')
        self.checkpoint = dict(gcode_sha256=hashlib.sha256((self.root/'plate_1.gcode').read_bytes()).hexdigest())
        self.persist()

    def persist(self):
        self.db.execute('INSERT OR REPLACE INTO checkpoint VALUES (1,?)', (json.dumps(self.checkpoint),))
        self.db.commit()

    def save(self):
        self.status['updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
        tmp = self.root/'status.json.tmp'
        tmp.write_text(json.dumps(self.status, indent=2))
        tmp.replace(self.root/'status.json')
        self.last_save = time.monotonic()

    def exchange(self, cmd, numbered=True, timeout=300):
        if self.stopping:
            raise RuntimeError('Stop requested')
        if numbered:
            self.number += 1
            body = f'N{self.number} {cmd}'.encode('ascii')
            packet = body + b'*' + str(functools.reduce(operator.xor, body, 0)).encode() + b'\n'
        else:
            packet = (cmd+'\n').encode('ascii')
        self.s.write(packet)
        deadline = time.monotonic()+timeout
        retries = 0
        resend = False
        responses = []
        while time.monotonic() < deadline:
            if self.stopping:
                raise RuntimeError('Stop requested')
            line = self.s.readline().decode('ascii', errors='replace').strip()
            if not line:
                continue
            responses.append(line)
            if 'T:' in line and 'B:' in line:
                self.status['temperature'] = line
            if not line.startswith('ok'):
                print('RX', line, flush=True)
            if time.monotonic()-self.last_save >= 1:
                self.save()
            match = re.search(r'(?:Resend:|rs\s+)(\d+)', line, re.I)
            if match:
                if not numbered or int(match[1]) != self.number or retries >= 3:
                    raise RuntimeError(f'Cannot recover serial sequence: {line}')
                resend = True
                continue
            lower = line.lower()
            if lower.startswith('error:') and not any(x in lower for x in ['checksum', 'line number', 'no checksum']):
                raise RuntimeError(line)
            if any(x in lower for x in ['kill() called', 'thermal runaway', 'heating failed', '//action:cancel', '//action:pause', 'unknown command']):
                raise RuntimeError(line)
            if line.startswith('ok'):
                if resend:
                    retries += 1
                    resend = False
                    self.s.write(packet)
                    continue
                return responses
        raise TimeoutError(f'No acknowledgement for {cmd}')

    def handle(self, request):
        action = request.get('action')
        if action == 'speed':
            value = request.get('percent')
            if isinstance(value, bool) or not isinstance(value, int) or not 25 <= value <= 200:
                raise ValueError('Speed percentage must be an integer from 25 to 200')
            self.exchange(f'M220 S{value}')
            self.status['speed_percent'] = value
            return dict(speed_percent=value)
        if action == 'query':
            return dict(temperatures=self.exchange('M105'), position=self.exchange('M114'),
                        note='Position is firmware-reported; acknowledged G-code may still be buffered.')
        if action == 'pause':
            self.exchange('M400')
            self.paused = True
            self.status['state'] = 'paused'
            return dict(note='Motion buffer drained; heaters remain on. Resume through this host only.')
        if action == 'resume':
            self.paused = False
            self.status['state'] = 'printing'
            return dict(note='Continuing the same in-memory job without homing.')
        raise ValueError('Allowed actions: speed, query, pause, resume')

    def controls(self):
        for path in sorted((self.root/'controls').glob('*.json')):
            claimed = path.with_suffix('.processing')
            path.rename(claimed)
            try:
                request = json.loads(claimed.read_text())
                # Validate before any printer write; communication faults fail the job.
                if request.get('action') not in ['speed','query','pause','resume']:
                    raise ValueError('Unsupported action')
                result = dict(ok=True, **self.handle(request))
            except (ValueError, TypeError, AttributeError) as exc:
                result = dict(ok=False, error=str(exc))
            except Exception as exc:
                (self.root/'control-results'/path.name).write_text(json.dumps(dict(ok=False,error=str(exc))))
                raise
            result['updated'] = time.strftime('%Y-%m-%d %H:%M:%S')
            (self.root/'control-results'/path.name).write_text(json.dumps(result,indent=2))
            claimed.unlink()
            print('CONTROL', path.name, result, flush=True)
            self.save()

    def run(self):
        self.exchange('M115',numbered=False,timeout=30)
        self.exchange('M110 N0',numbered=False,timeout=30)
        self.exchange('M155 S10')
        self.exchange('M75')
        lines = (self.root/'plate_1.gcode').read_text().splitlines()
        def command(raw):
            cmd = raw.split(';')[0].strip()
            return '' if cmd.startswith('M73 ') else cmd
        self.status.update(total_commands=sum(bool(command(x)) for x in lines),
                           total_file_lines=len(lines),state='printing',
                           started=time.strftime('%Y-%m-%d %H:%M:%S'))
        self.save()
        for file_line, raw in enumerate(lines,1):
            self.controls()
            while self.paused:
                if self.stopping:
                    raise RuntimeError('Stop requested')
                self.controls()
                if time.monotonic()-self.last_save >= 1:
                    self.save()
                time.sleep(.1)
            if raw.startswith(';LAYER_CHANGE'):
                self.status['layer'] += 1
            if raw.startswith(';Z:'):
                self.status['z'] = float(raw[3:])
            if raw.startswith(';TYPE:'):
                self.status['feature'] = raw[6:]
            cmd = command(raw)
            if not cmd:
                continue
            self.status['pending_file_line'] = file_line
            self.status['pending_command'] = cmd
            self.checkpoint['sent'] = dict(file_line=file_line,command=cmd,serial_line=self.number+1)
            self.persist()
            if cmd.startswith(('M190','M109','G28')):
                self.status['stage'] = cmd
                self.save()
            self.exchange(cmd)
            if cmd.startswith('M220 S'):
                self.status['speed_percent'] = int(cmd.split('S', 1)[1].split()[0])
            self.status['acknowledged'] += 1
            self.status['file_line'] = file_line
            self.status['last_command'] = cmd
            self.status['progress_percent'] = round(100*self.status['acknowledged']/self.status['total_commands'],2)
            self.checkpoint['acknowledged'] = dict(file_line=file_line,command=cmd,serial_line=self.number,
                                                   layer=self.status['layer'],z=self.status.get('z'))
            self.persist()
            if time.monotonic()-self.last_save >= 1:
                self.save()
        self.exchange('M400')
        self.exchange('M77')
        self.exchange('M155 S0')
        self.exchange('M105')
        self.status['state'] = 'completed'
        print('COMPLETED',flush=True)
        self.save()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--job',type=Path,required=True)
    parser.add_argument('--port',required=True)
    args = parser.parse_args()
    root=args.job.resolve()
    if (root/'status.json').exists() or (root/'progress.sqlite3').exists():
        raise SystemExit('Existing job state: refusing replay. Use a fresh job directory.')
    awake=subprocess.Popen(['/usr/bin/caffeinate','-i','-s','-w',str(os.getpid())])
    connection=None
    host=None
    try:
        connection=serial.Serial(args.port,115200,timeout=.5,write_timeout=5,exclusive=True)
        host=Host(root,connection)
        def stop(signum,frame): host.stopping=True
        signal.signal(signal.SIGTERM,stop)
        signal.signal(signal.SIGINT,stop)
        host.save()
        time.sleep(2)
        connection.reset_input_buffer()
        host.run()
    except Exception as exc:
        print('FAILED',str(exc),flush=True)
        if host:
            host.status.update(state='stopped' if host.stopping else 'failed',error=str(exc))
            host.save()
        if connection and connection.is_open:
            try:
                connection.write(b'M110 N0\nM410\nM104 S0\nM140 S0\nM106 S0\nM155 S0\n')
                connection.flush()
            except Exception:
                pass
        raise
    finally:
        if host: host.db.close()
        if connection: connection.close()
        awake.terminate()

if __name__ == '__main__': main()
