"""Drawing helpers for electronics guides: wires, pins, parts, meter, soldering iron, strip board."""
from .style import *  # noqa: F401,F403

RED, INK = "#c4161c", "#111"
EXTRA_CSS = '''
svg .pw{stroke:#c4161c;stroke-width:3.2}svg .gn{stroke:#111;stroke-width:3.2}svg .sg{stroke:#555;stroke-width:2.4}
svg .pin{fill:#fff;stroke:#111;stroke-width:1.6}svg .pin.y{fill:#ffd23f}
svg .lbl.r{fill:#c4161c}svg .lbl.b{font-weight:700}svg .lbl.m{font-size:11px;fill:#555}
svg .big{font:700 26px "Noto Sans",Verdana,sans-serif;fill:#111}
svg .ok{fill:none;stroke:#111;stroke-width:3}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:8px}
.two>*{min-width:0}
.yes,.no{display:flex;gap:10px;align-items:flex-start;border:2px solid var(--ink);padding:8px 12px;margin-top:10px;font-size:15px}
.yes b,.no b{flex:none;width:26px;height:26px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;background:var(--ink);color:var(--paper)}
.no{border-style:dashed}
'''

def wire(pts, kind="sg", dots=()):
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    o = f'<path class="o {kind}" d="{d}"/>'
    for x, y in dots:
        o += f'<circle cx="{x}" cy="{y}" r="4" fill="#111"/>'
    return o

def pin(x, y, hi=False):
    return f'<circle class="pin{" y" if hi else ""}" cx="{x}" cy="{y}" r="5"/>'

LEFT = ["EN", "MS1", "MS2", "RX", "TX", "CLK", "STEP", "DIR"]
RIGHT = ["VS", "GND", "A2", "A1", "B1", "B2", "VIO", "GND"]

class Driver:
    """TMC2209 module, drawn as in the pinout photo. Pin positions are in .p."""
    def __init__(self, ox, oy, s=13, hi=(), label=True, name=None):
        self.ox, self.oy, self.s = ox, oy, s
        w, h = 15.24*s, 20.32*s
        self.w, self.h = w, h
        self.p = {}
        o = f'<rect class="o w" x="{ox}" y="{oy}" width="{w}" height="{h}" rx="3"/>'
        o += f'<rect class="o g" x="{ox+w/2-14}" y="{oy+h/2-14}" width="28" height="28"/>'
        for i, n in enumerate(LEFT):
            x, y = ox + 1.27*s, oy + (i+.5)*2.54*s
            self.p[n] = (x, y)
            o += pin(x, y, n in hi)
            if label: o += txt(x - 12, y + 4, n, "end", "lbl m")
        for i, n in enumerate(RIGHT):
            x, y = ox + w - 1.27*s, oy + (i+.5)*2.54*s
            key = n if n != "GND" else ("GND1" if i == 1 else "GND2")
            self.p[key] = (x, y)
            o += pin(x, y, key in hi or n in hi and n != "GND")
            if label: o += txt(x + 12, y + 4, n, "start", "lbl m")
        if name:
            o += txt(ox + w/2, oy + h + 22, name, "middle", "lbl b")
        self.svg = o

def cap(x, y, s=1, hi=True, long_plus=True):
    """Electrolytic can standing up, long leg left (+), striped side right (-). Legs down."""
    o = f'<g transform="translate({x},{y}) scale({s})">'
    o += '<rect class="o w" x="-14" y="-46" width="28" height="46" rx="3"/>'
    o += '<rect class="o g" x="6" y="-46" width="8" height="46" rx="2"/>'
    o += '<line class="o" x1="-6" y1="0" x2="-6" y2="34"/><line class="o" x1="6" y1="0" x2="6" y2="22"/>'
    o += '</g>'
    return o

def resistor(x, y, bands=("#6b3a1a", "#111", "#c4161c"), s=1):
    o = f'<g transform="translate({x},{y}) scale({s})"><line class="o" x1="-40" y1="0" x2="-20" y2="0"/><line class="o" x1="20" y1="0" x2="40" y2="0"/>'
    o += '<rect class="o w" x="-20" y="-8" width="40" height="16" rx="6"/>'
    for i, c in enumerate(bands):
        o += f'<rect x="{-12+i*8}" y="-8" width="4" height="16" fill="{c}"/>'
    return o + '</g>'

def lead(label_xy, text, kind=""):
    x, y = label_xy
    return txt(x, y, text, "middle", "lbl " + kind)

def meter(x, y, mode="beep", s=1):
    o = f'<g transform="translate({x},{y}) scale({s})"><rect class="o w" x="-34" y="-56" width="68" height="112" rx="8"/><rect class="o g" x="-24" y="-46" width="48" height="26"/>'
    o += '<circle class="o w" cx="0" cy="12" r="15"/><line class="o" x1="0" y1="12" x2="8" y2="3"/>'
    o += '<circle class="o" cx="-16" cy="44" r="4"/><circle class="o" cx="16" cy="44" r="4"/></g>'
    return o

def iron(x, y, s=1, hot=True):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect class="o w" x="-6" y="-80" width="12" height="60" rx="3"/>'
            f'<polygon class="o y" points="-5,-20 5,-20 1.5,0 -1.5,0"/></g>')

def board_strip(x, y, cols, rows, pitch=14, solid=True):
    """Small piece of perfboard seen from above."""
    w, h = (cols-1)*pitch + 24, (rows-1)*pitch + 24
    o = f'<rect class="o g" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"/>'
    for r in range(rows):
        for c in range(cols):
            o += f'<circle cx="{x+12+c*pitch}" cy="{y+12+r*pitch}" r="3.2" fill="#fff" stroke="#111" stroke-width="1.2"/>'
    return o

def ytag(label, color="y"):
    return f'<span class="tag">{label}</span>'

def yes(s): return f'<div class="yes"><b>✓</b><span>{s}</span></div>'
def no(s): return f'<div class="no"><b>✕</b><span>{s}</span></div>'
def img(src, alt):
    """A wiring diagram or photo by its path relative to the guide page."""
    return f'<img src="{src}" alt="{alt}" style="width:100%;height:auto;border:1.5px solid var(--rule);background:#fff">'

def epage(title, sub, body, nav="", after=""):
    return page(title, sub, body, nav, after).replace("</style>", EXTRA_CSS + "</style>", 1)
