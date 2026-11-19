"""Concept sketches (schematic sections, not to scale) for foam-pump-bottle-adapter."""
import sys
from pathlib import Path
OUT, FRAG = Path(sys.argv[1]), Path(sys.argv[2])
STYLE = """<style>
.paper{fill:#f4f6f7}.glass{fill:none;stroke:#7a8f9a;stroke-width:4;stroke-linejoin:round}
.pump{fill:#ffffff;stroke:#5b6670;stroke-width:1.5}.print{fill:#e8792b;stroke:#8f4410;stroke-width:1.5}
.print2{fill:#f3b27f;stroke:#8f4410;stroke-width:1.5}.far{fill:#f3b27f;stroke:#8f4410;stroke-width:1;stroke-dasharray:4 3;opacity:.7}
.metal{fill:#1f2428;stroke:#1f2428;stroke-width:1}.wall{fill:#d5dadd;stroke:none}
.thread{fill:none;stroke:#1f2428;stroke-width:3.2;stroke-dasharray:2.5 2.5}
.axis{stroke:#9aa5ad;stroke-width:1;stroke-dasharray:10 4 2 4;fill:none}
.lead{stroke:#3a4249;stroke-width:1;fill:none}.dash{fill:none;stroke:#3a4249;stroke-width:1.2;stroke-dasharray:4 3}
.bad{stroke:#c8102e;stroke-width:3.5;fill:none;stroke-linecap:round}
text{font:13px -apple-system,'Helvetica Neue',Arial,sans-serif;fill:#1f2428}.t{font-weight:700;font-size:15px}.badt{fill:#c8102e;font-weight:700}
</style>"""

class D:
    def __init__(s, w, h, cx, title):
        s.w, s.h, s.cx, s.e, s.top = w, h, cx, [], []
        s.title = title
    def add(s, x): s.e.append(x)
    def sym(s, r0, r1, y0, y1, cls, cx=None):
        cx = cx or s.cx
        if r0 == 0: s.rect(cx - r1, y0, 2 * r1, y1 - y0, cls)
        else:
            s.rect(cx - r1, y0, r1 - r0, y1 - y0, cls); s.rect(cx + r0, y0, r1 - r0, y1 - y0, cls)
    def rect(s, x, y, w, h, cls, rx=0): s.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>')
    def thread(s, r, y0, y1, cx=None):
        cx = cx or s.cx
        for x in (cx - r, cx + r): s.add(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" class="thread"/>')
    def axis(s, y0, y1, cx=None): s.add(f'<line x1="{cx or s.cx}" y1="{y0}" x2="{cx or s.cx}" y2="{y1}" class="axis"/>')
    def bottle(s, r, top, sh, body, bot=None, cx=None):
        cx = cx or s.cx; bot = bot or s.h - 14
        for k in (-1, 1):
            s.add(f'<path d="M{cx+k*r},{top} V{sh} L{cx+k*body},{sh+26} V{bot}" class="glass"/>')
    def pump(s, rin, rout, ybot, h=26, cx=None, tube=None):
        cx = cx or s.cx; top = ybot - h
        s.rect(cx - 5, top, 10, 50 + h, "pump"); s.rect(cx - 2, top + 50 + h, 4, (tube or s.h - 30) - (top + 50 + h), "pump")
        s.sym(rin, rout, top, ybot, "pump", cx); s.rect(cx - rout, top - 5, 2 * rout, 5, "pump")
        s.rect(cx - rout - 6, top - 27, 2 * rout + 12, 22, "pump", 5)
        s.rect(cx - 9, top - 60, 18, 33, "pump")
        s.add(f'<path d="M{cx+13},{top-60} h-52 q-10,0 -12,12 h8 q2,-5 8,-5 h48 z" class="pump" transform="translate(0,-7)"/>')
        return top - 67
    def bracket(s, hole, y, wallx, cx=None):
        cx = cx or s.cx
        s.rect(wallx, 20, 12, s.h - 30, "wall")
        s.rect(cx - hole - 22, y, 22, 5, "metal"); s.rect(cx + hole, y, wallx - cx - hole, 5, "metal"); s.rect(wallx - 5, y, 5, 95, "metal")
    def label(s, x, y, tx, ty, text, anchor="start", cls=""):
        dx = 5 if anchor == "start" else -5
        s.top.append(f'<path d="M{x},{y} L{tx},{ty}" class="lead"/><circle cx="{x}" cy="{y}" r="2" fill="#3a4249" class="dot"/>')
        for i, line in enumerate(text.split("\n")):
            s.top.append(f'<text x="{tx+dx}" y="{ty+4+i*15}" text-anchor="{anchor}" class="{cls}">{line}</text>')
    def cross(s, x, y, r=8): s.top.append(f'<path d="M{x-r},{y-r} L{x+r},{y+r} M{x-r},{y+r} L{x+r},{y-r}" class="bad"/>')
    def svg(s, style=True):
        body = "".join(s.e + s.top)
        head = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" role="img" aria-label="{s.title}">'
        if style: head += STYLE + f'<rect width="{s.w}" height="{s.h}" class="paper"/>'
        return head + f'<text x="14" y="24" class="t">{s.title}</text>' + body + "</svg>"

W, H, CX, YR, HOLE, WALL = 660, 430, 330, 240, 19, 430
def base(title, h=H):
    d = D(W, h, CX, title); d.bracket(HOLE, YR, WALL); d.axis(40, h - 10); return d
out = {}

# problem A: narrow neck
d = base("Problem A: narrow-neck bottle")
d.bottle(14, 196, 262, 62); d.thread(15.5, 200, 232)
d.pump(21, 25, 176)
d.cross(CX - 18, 186); d.cross(CX + 18, 186)
d.label(CX - 14, 215, 200, 200, "neck passes the hole", "end")
d.label(CX + 23, 165, 478, 120, "pump thread is far\nwider than the neck:\nnothing to screw onto", "start", "badt")
d.label(CX - 30, YR + 2, 200, 300, "bracket ring", "end")
d.label(WALL + 6, 80, 478, 60, "wall")
out["0a-problem-narrow-neck"] = d

# problem B: wide neck
d = base("Problem B: wide-neck bottle")
d.bottle(22, YR + 9, 290, 62); d.thread(23.5, YR + 13, 280)
d.pump(23.5, 28, 190)
d.cross(CX - 21, YR + 7); d.cross(CX + 21, YR + 7)
d.label(CX - 22, YR + 20, 200, 300, "neck is wider than\nthe hole: stuck below", "end", "badt")
d.label(CX + 26, 178, 478, 120, "pump fits this neck,\nbut cannot reach it")
out["0b-problem-wide-neck"] = d

# 1: nested thread sleeve
d = base("1. Thread sleeve (nested)")
d.bottle(14, 200, 264, 62)
d.sym(15.5, 21, 198, YR, "print"); d.sym(15.5, 31, YR - 5, YR, "print")
d.thread(15.5, 202, YR - 2); d.thread(22, 200, YR - 7)
d.pump(22.5, 27, YR - 5, h=42)
d.label(CX - 18, 222, 200, 190, "printed sleeve: thread inside\nfor the neck, thread outside\nfor the pump", "end")
d.label(CX - 29, YR - 3, 200, 262, "flange rests on the ring,\nbottle hangs from it", "end")
d.label(CX + 25, 215, 478, 150, "pump screws over\nthe sleeve: adds\nalmost no height")
d.label(CX + 14, 256, 478, 300, "narrow neck comes\nup through the hole")
out["1-thread-sleeve"] = d

# 2: stacked step-up
d = base("2. Step-up adapter (stacked)")
d.bottle(14, 204, 264, 62)
d.sym(15.5, 27, 202, YR, "print"); d.sym(7, 27, 194, 202, "print"); d.sym(7, 21, 160, 194, "print")
d.thread(15.5, 206, YR - 2); d.thread(22, 163, 192)
d.pump(22.5, 27, 194, h=34)
d.label(CX - 24, 220, 200, 230, "lower half: cap that\nscrews onto the neck", "end")
d.label(CX - 16, 178, 200, 150, "upper half: a copy of\nthe wide neck the\npump was made for", "end")
d.label(CX + 25, 180, 478, 200, "pump sits about one\nneck height taller")
d.label(CX + 5, 300, 478, 300, "dip tube now ends\nhigher in the bottle")
out["2-step-up-adapter"] = d

# 3: bulkhead coupler
d = base("3. Through-hole coupler (two parts)")
d.bottle(22, YR + 18, 292, 62); d.thread(23.5, YR + 21, YR + 42)
d.sym(23.5, 30, YR + 5, YR + 44, "print2"); d.sym(17, 30, YR + 5, YR + 18, "print2")
d.sym(11, 17, YR - 8, YR + 17, "print"); d.sym(11, 32, YR - 8, YR, "print"); d.sym(11, 22, YR - 40, YR - 8, "print")
d.thread(17, YR + 6, YR + 16); d.thread(22.5, YR - 38, YR - 10)
d.pump(23, 28, YR - 8, h=34)
d.label(CX - 30, YR - 4, 200, 190, "top part: drops through\nthe hole from above,\npump screws onto it", "end")
d.label(CX - 28, YR + 30, 200, 300, "bottom part: cap on the\nwide neck; the two screw\ntogether and pinch the ring", "end")
d.label(CX + 8, 215, 478, 130, "bore must clear the\npump's stem")
d.label(CX + 5, 330, 478, 330, "pump sits higher:\ndip tube needs\nextending")
out["3-through-hole-coupler"] = d

# 5: slide-on saddle
d = base("5. Slide-on saddle")
d.bottle(22, YR + 15, 292, 62); d.thread(23.5, YR + 19, YR + 42)
d.sym(23.5, 30, YR + 5, YR + 46, "print"); d.sym(18, 30, YR + 5, YR + 15, "print")
d.sym(18, 30, YR - 9, YR, "print"); d.sym(18, 24, YR - 40, YR - 9, "print")
d.add(f'<path d="M{CX-30},{YR-9} H{CX-49} V{YR+15} H{CX-30} V{YR+5} H{CX-41} V{YR} H{CX-30} Z" class="print"/>')
d.thread(25, YR - 38, YR - 11)
d.pump(25.5, 30, YR - 9, h=34); d.rect(CX - 16, YR - 43, 32, 75, "pump")
d.label(CX - 45, YR + 2, 200, 215, "web joins top and bottom\naround the front of the ring", "end")
d.label(CX - 21, YR - 25, 200, 150, "top: thread for the pump", "end")
d.label(CX - 27, YR + 30, 200, 310, "bottom: cap thread for\nthe bottle, under the ring", "end")
d.label(CX + 12, YR + 3, 478, 130, "pump body drops through\nthe hole and pins the\nsaddle in place")
d.label(CX + 34, YR + 2, 478, 300, "slot is open at the back:\nslides on from the front")
out["5-slide-on-saddle"] = d
# 6: hanging collar
d = base("6. Hanging collar")
d.bottle(22, YR + 5, 292, 62); d.thread(23.5, YR + 12, YR + 38)
d.sym(23.5, 30, YR + 5, YR + 42, "print")
d.add(f'<path d="M{CX-30},{YR+5} H{CX-49} V{YR-13} H{CX-32} V{YR-9} L{CX-41},{YR} V{YR+5} Z" class="print"/>')
d.pump(25.5, 30, YR - 13, h=34); d.rect(CX - 16, YR - 47, 32, 85, "pump")
d.label(CX - 38, YR - 9, 200, 190, "lip hooks over the ring's\nfront and side edges", "end")
d.label(CX - 27, YR + 30, 200, 310, "threaded collar: the bottle\nscrews up into it", "end")
d.label(CX + 20, YR + 6, 478, 310, "top of the neck presses\nagainst the metal ring\nand clamps everything")
d.label(CX + 10, YR - 30, 478, 130, "pump drops through the\nhole and rests on the lips.\nLift it out to refill")
out["6-hanging-collar"] = d
# 7: hidden holder for the glass bottle (own wall holder)
d = D(W, 470, CX, "7. Hidden holder for the glass bottle")
d.rect(WALL, 20, 12, 440, "wall"); d.axis(40, 460)
NY, FY = 190, 400          # neck loop and foot levels
for k in (-1, 1):
    d.add(f'<path d="M{CX+k*20},{NY-22} V{NY+16} L{CX+k*46},{NY+40} V{FY} H{CX}" class="glass"/>')
d.thread(21.5, NY-20, NY-6)
d.rect(WALL - 7, NY, 7, FY - NY + 7, "print")                       # spine on the wall
d.rect(CX + 24, NY, WALL - 7 - CX - 24, 6, "print"); d.rect(CX - 30, NY, 6, 6, "print")   # loop round the neck
d.rect(CX - 30, FY + 2, WALL - 7 - CX + 30, 5, "print")              # foot under the base
d.pump(21.5, 27, NY - 2, h=24, tube=FY - 14)
d.label(CX - 27, NY + 3, 200, 130, "closed loop round the neck,\nhidden under the pump collar", "end")
d.label(CX - 10, FY + 5, 200, 440, "small foot carries the weight,\nhidden under the base", "end")
d.label(WALL - 4, 300, 478, 250, "spine on the wall,\nhidden behind\nthe bottle")
d.label(CX + 27, NY - 16, 478, 110, "with the pump screwed on\nthe bottle cannot leave")
out["7-hidden-holder"] = d

for name, d in out.items():
    (OUT / f"{name}.svg").write_text(d.svg(True)); (FRAG / f"{name}.svg").write_text(d.svg(False))
print(len(out), "sketches")
