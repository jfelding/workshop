"""Drawing helpers and page style for IKEA-style assembly guides (methods/assembly-guides.md).

A guide is a Python module whose build(nav) returns one HTML page from page(), step(), warn(),
svg() and the icons here; workshop.guides.book numbers the chapters and writes the files.
"""
import math

def hexp(cx, cy, r, rot=30):
    pts = [(cx + r*math.cos(math.radians(rot + 60*i)), cy + r*math.sin(math.radians(rot + 60*i))) for i in range(6)]
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)

def nut(cx, cy, r, cls="w"):
    return f'<polygon class="o {cls}" points="{hexp(cx,cy,r)}"/><circle class="o w" cx="{cx}" cy="{cy}" r="{r*0.42:.1f}"/>'

def washer(cx, cy, r, cls="w"):
    return f'<circle class="o {cls}" cx="{cx}" cy="{cy}" r="{r}"/><circle class="o w" cx="{cx}" cy="{cy}" r="{r*0.45:.1f}"/>'

DEFS = '''<defs>
<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#111"/></marker>
</defs>'''

def svg(vb, body, label, cls=""):
    return f'<svg class="{cls}" viewBox="{vb}" role="img" aria-label="{label}">{DEFS}{body}</svg>'

#: Directory holding the guide's CAD-rendered drawings; set once per project.
VIEWS = None

def view(name, views=None):
    """A drawing rendered from the CAD (workshop.cad.render) and saved as <VIEWS>/<name>.svg."""
    import os
    d = views or VIEWS
    if d is None:
        raise RuntimeError("set workshop.guides.style.VIEWS to the project's views directory")
    with open(os.path.join(d, f'{name}.svg')) as f:
        return f.read()

def arrow(d, both=False):
    m = ' marker-start="url(#ah)"' if both else ''
    return f'<path class="o a" d="{d}" marker-end="url(#ah)"{m}/>'

def txt(x, y, s, anchor="middle", cls="lbl"):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{s}</text>'

# ---------- icons for the parts sheet ----------
def screw_icon(L, head=True, thread=True, cls="w"):
    o = ""
    x = 0
    if head:
        o += f'<rect class="o {cls}" x="0" y="-9" width="9" height="18"/>'
        x = 9
    o += f'<rect class="o {cls}" x="{x}" y="-5" width="{L}" height="10"/>'
    if thread:
        for i in range(x+4, x+L-2, 5):
            o += f'<line class="o t" x1="{i}" y1="-5" x2="{i+3}" y2="5"/>'
    return o

CSS = '''
:root{--paper:#fffefa;--ink:#111;--grey:#e4e4e0;--hi:#ffd23f;--faint:#6b6b66;--rule:#cfcfc8;color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.45 "Noto Sans",Verdana,Arial,sans-serif;padding-inline:20px}
main{max-width:780px;margin:0 auto;padding-block:32px 72px;overflow-wrap:anywhere}
h1{font-size:clamp(26px,5vw,38px);margin:0 0 6px;line-height:1.1;text-wrap:balance}
.sub{margin:0 0 20px;color:var(--faint)}
.key{display:flex;gap:18px;flex-wrap:wrap;margin:0 0 36px;font-size:14px}
.key span{display:inline-flex;align-items:center;gap:8px}
.sw{width:22px;height:14px;border:2px solid var(--ink)}
.sw.y{background:var(--hi)}.sw.g{background:var(--grey)}.sw.w{background:#fff}
.sheet{border-top:3px solid var(--ink);padding-top:22px;margin-top:40px}
.sheet h2{margin:0 0 16px;font-size:14px;letter-spacing:.12em;text-transform:uppercase}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,150px),1fr));gap:14px}
.card{border:1.5px solid var(--rule);padding:8px 8px 10px;text-align:center}
.card svg{width:100%;height:auto;display:block}
.cnt{font-weight:700;font-size:28px;line-height:1}
.nm{font-size:13px;color:var(--faint);margin-top:2px}
.step{border-top:3px solid var(--ink);margin-top:44px;padding-top:16px}
.head{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:start;gap:10px 16px;margin-bottom:10px}
.num{font-weight:700;font-size:64px;line-height:.9;min-width:40px;white-space:nowrap}
.say{margin:6px 0 0;font-size:18px;font-weight:700;text-wrap:balance}
.tag{margin-left:auto;border:2px solid var(--ink);padding:2px 10px;font-weight:700;font-size:20px;white-space:nowrap}
.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:8px}
.cards>*,.pair>*{min-width:0}
svg{max-width:100%;height:auto;display:block;width:100%}
.warn{display:flex;gap:12px;align-items:flex-start;border:2px solid var(--ink);padding:10px 14px;margin-top:12px;font-size:15px}
.warn b{display:inline-flex;align-items:center;justify-content:center;flex:none;width:26px;height:26px;border-radius:50%;background:var(--ink);color:var(--paper)}
ul.chk{list-style:none;padding:0;margin:10px 0 0;font-size:17px}
ul.chk li{padding-left:34px;position:relative;margin:6px 0}
ul.chk li::before{content:"";position:absolute;left:2px;top:3px;width:18px;height:18px;border:2px solid var(--ink)}
svg .o{fill:none;stroke:#111;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
svg .k{stroke-width:4}
svg .g{fill:var(--grey)}svg .y{fill:var(--hi)}svg .w{fill:#fff}
svg .d{stroke-dasharray:6 5;stroke-width:1.6}
svg .t{stroke-width:1.2}
svg .a{stroke-width:2.5}
svg .lbl{font:600 15px "Noto Sans",Verdana,sans-serif;fill:#111;stroke:none}
svg .lbl.s{font-weight:400;font-size:12.5px;fill:#555}
.after{margin-top:48px;border-top:3px solid var(--ink);padding-top:16px;font-size:15px}
.after p{margin:6px 0}
@media(max-width:600px){.head{grid-template-columns:auto minmax(0,1fr)}.head .tag{grid-column:2;justify-self:start;margin-left:0}.num{font-size:48px}}
'''

# Include labels outside the original drawing bounds, with room for strokes and arrows.
# Refit after fonts load because their metrics determine the text bounds.
FIT = '''<script>
function fitDrawings(){document.querySelectorAll('svg[viewBox]').forEach(function(s){
var b=s.getBBox(),v=s.viewBox.baseVal,p=10;
var x0=Math.min(v.x,b.x-p),y0=Math.min(v.y,b.y-p);
var x1=Math.max(v.x+v.width,b.x+b.width+p),y1=Math.max(v.y+v.height,b.y+b.height+p);
s.setAttribute('viewBox',x0+' '+y0+' '+(x1-x0)+' '+(y1-y0));
});}
fitDrawings();window.addEventListener('load',fitDrawings);
if(document.fonts)document.fonts.ready.then(fitDrawings);
</script>'''

def step(n, say, figs, tag=None, extra=""):
    t = f'<div class="tag">{tag}</div>' if tag else ''
    return f'<section class="step"><div class="head"><div class="num">{n}</div><p class="say">{say}</p>{t}</div>{figs}{extra}</section>'

def warn(s):
    return f'<div class="warn"><b>!</b><span>{s}</span></div>'


class Parts:
    """The "You need" sheet of one guide."""
    def __init__(self): self.cards = []
    def card(self, count, inner, name, vb="0 0 140 90"):
        self.cards.append(f'<div class="card"><svg viewBox="{vb}" role="img" aria-label="{name}">{inner}</svg><div class="cnt">{count}×</div><div class="nm">{name}</div></div>')
    def sheet(self, note=""):
        n = f'<p class="sub" style="margin-top:14px;font-size:14px">{note}</p>' if note else ''
        return f'<section class="sheet"><h2>You need</h2><div class="cards">{"".join(self.cards)}</div>{n}</section>'

KEY = '<div class="key"><span><i class="sw y"></i>this step</span><span><i class="sw g"></i>already fitted</span><span><i class="sw w"></i>other parts</span></div>'

def page(title, sub, body, nav="", after=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<main>
{nav}<h1>{title}</h1>
<p class="sub">{sub}</p>
{KEY}
<p class="sub" style="margin-top:-18px">Drawings are simple sketches, not to scale.</p>
{body}
{after}
</main>
{FIT}
</body>
</html>'''
