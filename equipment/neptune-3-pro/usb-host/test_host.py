import contextlib
import io
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from host import Host

class FakeSerial:
    def __init__(self,responses=None):
        self.writes=[]
        self.responses=list(responses or [])
    def write(self,packet): self.writes.append(packet)
    def readline(self): return self.responses.pop(0) if self.responses else b'ok\n'

class HostTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        (self.root/'plate_1.gcode').write_text('G21\n;LAYER_CHANGE\n;Z:0.2\n;TYPE:Brim\nG1 X10 Y20 Z.2 E.1\nM73 P1 R1\nM104 S0\n')
        self.serial=FakeSerial();self.host=Host(self.root,self.serial)
    def tearDown(self): self.host.db.close();self.tmp.cleanup()
    def test_live_controls_use_one_connection(self):
        for name,req in [('01',{'action':'speed','percent':150}),('02',{'action':'pause'}),('03',{'action':'resume'})]:
            (self.root/'controls'/f'{name}.json').write_text(json.dumps(req))
        self.host.controls()
        text=b''.join(self.serial.writes)
        self.assertIn(b'M220 S150',text);self.assertIn(b'M400',text)
        self.assertFalse(self.host.paused);self.assertEqual(self.host.status['speed_percent'],150)
        self.assertTrue(json.loads((self.root/'control-results/01.json').read_text())['ok'])
    def test_invalid_controls_do_not_write(self):
        for request in [{'action':'speed','percent':False},{'action':'speed','percent':201},{'action':'home'}]:
            with self.assertRaises(ValueError):self.host.handle(request)
        self.assertEqual(self.serial.writes,[])
    def test_resend_repeats_same_packet(self):
        self.serial.responses=[b'Resend:1\n',b'ok\n',b'ok\n']
        self.host.exchange('G1 X1')
        self.assertEqual(len(self.serial.writes),2)
        self.assertEqual(*self.serial.writes)
    def test_fault_stops_exchange(self):
        self.serial.responses=[b'Error:Heating failed\n']
        with self.assertRaises(RuntimeError):self.host.exchange('M109 S210')
    def test_run_records_source_checkpoint_and_drains(self):
        self.host.run()
        checkpoint=json.loads(self.host.db.execute('SELECT data FROM checkpoint').fetchone()[0])
        self.assertEqual(checkpoint['acknowledged']['file_line'],7)
        self.assertEqual(checkpoint['acknowledged']['command'],'M104 S0')
        self.assertEqual(self.host.status['layer'],1)
        self.assertEqual(self.host.status['state'],'completed')
        text=b''.join(self.serial.writes)
        self.assertNotIn(b'M73 ',text);self.assertIn(b'M400',text)
    def test_disconnect_mid_job_preserves_sent_vs_acknowledged(self):
        original=self.serial.readline
        def read():
            if len(self.serial.writes)==6: raise OSError('Device not configured')
            return original()
        self.serial.readline=read
        with self.assertRaises(OSError):self.host.run()
        saved=json.loads(self.host.db.execute('SELECT data FROM checkpoint').fetchone()[0])
        self.assertEqual(saved['sent']['file_line'],5)
        self.assertEqual(saved['acknowledged']['file_line'],1)

    def test_disconnect_leaves_unacknowledged_sent_command(self):
        def failure(): raise OSError('Device not configured')
        self.serial.readline=failure
        with self.assertRaises(OSError):self.host.run()
        self.assertNotIn('acknowledged',self.host.checkpoint)

if __name__=='__main__': unittest.main()
