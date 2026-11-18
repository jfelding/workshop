from pathlib import Path
from collections import Counter
import re,json,hashlib,zipfile
p=Path(__file__).resolve().parent
if (p/'plate_1.orca.gcode').exists() or (p/'head-theta-gear-infill-first.orca.3mf').exists():
    raise SystemExit('Already reordered: use a freshly sliced job directory.')
original=(p/'plate_1.gcode').read_text()
lines=original.splitlines(keepends=True)
a=next(i for i,x in enumerate(lines) if x.startswith(';LAYER_CHANGE'))
b=next(i for i in range(a+1,len(lines)) if lines[i].startswith(';LAYER_CHANGE'))
layer=lines[a:b]
first_type=next(i for i,x in enumerate(layer) if x.startswith(';TYPE:'))
wall_start=next(i for i,x in enumerate(layer[:first_type]) if x.startswith('G1 X'))
bottom_type=next(i for i,x in enumerate(layer) if x.startswith(';TYPE:Bottom surface'))
bottom_start=max(i for i in range(bottom_type) if layer[i].startswith(';WIPE_END'))+1
following_type=next(i for i in range(bottom_type+1,len(layer)) if layer[i].startswith(';TYPE:'))
bottom_end=max(i for i in range(following_type) if layer[i].startswith(';WIPE_END'))+1
assert layer[bottom_start].startswith('G1 X') and layer[bottom_end].startswith('G1 X')
# Both complete groups begin retracted and finish retracted. Lift before each
# relocated group; its original absolute XY travel and unretract remain intact.
lift=[';REORDERED_FIRST_LAYER: bottom surface before outlines\n','G1 Z0.6 F300\n','G1 F3000\n']
new_layer=layer[:wall_start]+lift+layer[bottom_start:bottom_end]+lift+layer[wall_start:bottom_start]+layer[bottom_end:]
modified=''.join(lines[:a]+new_layer+lines[b:])
def paths(text):
 xyz=[0.,0.,0.];feed=0.;relative_e=False;absolute_xyz=False;events=[];layer_num=0;balance=0.;positions={}
 for line in text.splitlines():
  if line.startswith(';LAYER_CHANGE'):layer_num+=1
  c=line.split(';')[0].strip()
  if c=='G90':absolute_xyz=True
  if c=='M83':relative_e=True
  if not re.match(r'^G[01]\s',c):continue
  assert absolute_xyz and relative_e
  vals={k:float(v) for k,v in re.findall(r'([XYZEF])(-?\d*\.?\d+)',c)}
  before=tuple(xyz);xyz=[vals.get(k,xyz[i]) for i,k in enumerate('XYZ')];feed=vals.get('F',feed)
  if 'E' in vals and any(k in vals for k in 'XYZ'):
   events.append((layer_num,before,tuple(xyz),vals['E'],feed))
  elif 'E' in vals: events.append((layer_num,'extruder_only',vals['E'],feed))
 return events
before=Counter(paths(original));after=Counter(paths(modified));assert before==after,dict(removed=list((before-after).items())[:3],added=list((after-before).items())[:3])
features=[x.strip()[6:] for x in new_layer if x.startswith(';TYPE:')];assert features[0]=='Bottom surface'
assert ';TYPE:Brim' not in modified
(p/'plate_1.orca.gcode').write_text(original)
(p/'plate_1.gcode').write_text(modified)
archive=p/'head-theta-gear-infill-first.3mf';saved=p/'head-theta-gear-infill-first.orca.3mf';archive.rename(saved)
with zipfile.ZipFile(saved) as zin,zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as zout:
 for item in zin.infolist():
  data=zin.read(item.filename)
  if item.filename=='Metadata/plate_1.gcode':data=modified.encode()
  if item.filename=='Metadata/plate_1.gcode.md5':data=hashlib.md5(modified.encode()).hexdigest().encode()
  zout.writestr(item,data)
r=dict(first_layer_features=features,extrusion_paths_unchanged=True,extrusion_events=len(list(paths(original))),original_sha256=hashlib.sha256(original.encode()).hexdigest(),modified_sha256=hashlib.sha256(modified.encode()).hexdigest(),added_travel='0.6 mm lift before relocated first-layer groups')
(p/'reorder-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
