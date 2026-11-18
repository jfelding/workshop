"""Submit allowlisted commands to the existing host; never opens the serial port."""
import argparse
import json
from pathlib import Path
import time
import uuid

p=argparse.ArgumentParser()
p.add_argument('--job',type=Path,required=True)
p.add_argument('action',choices=['speed','query','pause','resume'])
p.add_argument('--percent',type=int)
a=p.parse_args()
status=json.loads((a.job/'status.json').read_text())
if status['state'] not in ['printing','paused']:
    raise SystemExit('Host is not running a controllable job')
request={'action':a.action}
if a.action=='speed':
    if a.percent is None or not 25<=a.percent<=200: raise SystemExit('--percent must be 25–200')
    request['percent']=a.percent
name=f'{time.time_ns()}-{uuid.uuid4().hex}.json'
path=a.job/'controls'/name
tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(request));tmp.replace(path)
print('Request:',name,flush=True)
result=a.job/'control-results'/name
for _ in range(150):
    if result.exists():
        data=json.loads(result.read_text());print(json.dumps(data,indent=2));raise SystemExit(0 if data['ok'] else 1)
    time.sleep(.1)
print('Pending. Check control-results; do not open another serial connection.')
