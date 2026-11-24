"""Pictures of the amber holder with the STAND-IN bottle and pump in place.

The holder and ring are the designed parts. The bottle and pump are the stand-in from amber_checks.py,
built from the measured bottle (shoulder and pump head estimated), and the wall is scenery.

    uv run python cad/amber_illustrate.py    # writes exports/preview.png and exports/amber-*.png
"""
import subprocess

from workshop.cad.geometry import box
from workshop.cad.render import View, render

import amber_checks as ac
import amber_holder as ah

OUT = ah.OUT
PRINT, GLASS, PUMP, WALL = (232, 121, 43), (128, 78, 36), (58, 60, 64), (214, 218, 221)
L = ah.LAYOUT
glass, pump_low, pump_head, info = ac.stand_in()
pump = pump_low + pump_head
wall = box(-70, 70, L["y_wall"], L["y_wall"] + 4, L["z_bot"] - 30, 190)


def scene(lift=0.0, forward=0.0, ring_lift=None, cut=False, with_wall=True):
    rl = lift if ring_lift is None else ring_lift
    items = [(ah.holder, PRINT), (ah.ring_fitted.translate((0, -forward, rl)), PRINT),
             (glass.translate((0, -forward, lift)), GLASS), (pump.translate((0, -forward, lift)), PUMP)]
    if with_wall:
        items.append((wall, WALL))
    if cut:   # keep the half at x >= 0
        keep = box(0, 200, -200, 200, -300, 300)
        items = [(s & keep, g) for s, g in items]
    return items


lift = ac.R["lift_to_remove_mm"]
key_rise = L["z_top"] - L["key_z0"] + 2
VIEWS = {
    "preview": ("Amber bottle on the printed holder (bottle and pump: stand-in from measurements)", scene(), View((-0.75, -1, 0.45)), 560),
    "amber-front": ("From the front: what shows", scene(), View((0, -1, 0.08)), 360),
    "amber-side": ("From the side", scene(with_wall=False), View((-1, 0, 0.05)), 420),
    "amber-section": ("Cut in half", scene(cut=True, with_wall=False), View((-1, -0.2, 0.15)), 420),
    "amber-out": (f"To take it out: lift {lift:.0f} mm, then forward", scene(lift=lift, forward=55, ring_lift=key_rise, with_wall=False), View((-0.9, -1, 0.35)), 560),
    "amber-parts": ("The two printed parts, as installed", [(ah.holder, PRINT), (ah.ring.translate((0, -60, 30)), PRINT)], View((-0.8, -1, 0.6)), 520),
}
OUT.mkdir(exist_ok=True)
for name, (title, items, view, width) in VIEWS.items():
    body, (w, h) = render(items, view, width=width)
    pad, head = 24, 44
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w + 2 * pad:.0f}" height="{h + head + pad:.0f}">'
           f'<rect width="100%" height="100%" fill="#f6f7f8"/>'
           f'<text x="{pad}" y="29" font-family="Helvetica, Arial, sans-serif" font-size="16" font-weight="700" fill="#1c2226">{title}</text>'
           f'<g transform="translate({pad},{head})">{body}</g></svg>')
    tmp = OUT / f"{name}.svg"
    tmp.write_text(svg)
    subprocess.run(["rsvg-convert", "-z", "2", str(tmp), "-o", str(OUT / f"{name}.png")], check=True)
    tmp.unlink()
    print("wrote", OUT / f"{name}.png")
