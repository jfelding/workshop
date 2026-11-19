"""Pictures of the hanging collar in place: assembled, from below, exploded, cut in half, and alone.

Only the collar is a designed part. Bracket, bottle and pump are drawn for context: their measured
interfaces come from measurements.py, everything in SCENERY below is made up for the picture
(bottle body, pump head, how far the bracket stands off the wall) and must not be used for design.

    uv run python cad/illustrate.py [--draft]     # writes exports/preview.png and exports/view-*.png
"""
import subprocess
from pathlib import Path

from build123d import Circle, Pos, Rectangle, extrude, fillet

from workshop.cad.geometry import box, cylinder
from workshop.cad.render import View, render

import hanging_collar as hc

dim, m = hc.dim, hc.m
OUT = Path(__file__).parents[1] / "exports"
SCENERY = dict(bottle_side=68, bottle_height=105, bottle_corner=9, wall_offset=42, flange_drop=55,
               pump_head_d=40, pump_stem_d=14, pump_stem_h=20, spout_len=38, pump_body_len=48)
S = SCENERY
PRINT, METAL, GLASS, PUMP = (232, 121, 43), (176, 182, 188), (222, 233, 238), (58, 60, 64)

t, hole, ring_w = hc.t, hc.hole, hc.ring_w
lift = dim("COLLAR_RING_LIFT")

# bracket: ring plate running back to a flange that drops down the wall
plate = extrude(Pos(0, 0, lift) * (hc.u_face(ring_w / 2, S["wall_offset"]) - Circle(hole / 2)), t)
flange = box(-ring_w / 2, ring_w / 2, S["wall_offset"] - t, S["wall_offset"], lift + t - S["flange_drop"], lift + t)
bracket = plate + flange

# bottle: measured neck, made-up body. Neck top touches the ring's underside.
neck_h = dim("WIDE_NECK_HEIGHT")
neck = cylinder(dim("WIDE_NECK_ROOT_OD") / 2, neck_h, "z", (0, 0, lift - neck_h / 2))
body = extrude(Pos(0, 0, lift - neck_h - S["bottle_height"]) * fillet(Rectangle(S["bottle_side"], S["bottle_side"]).vertices(), S["bottle_corner"]), S["bottle_height"])
bottle = neck + body - cylinder(dim("WIDE_NECK_BORE") / 2, neck_h + 30, "z", (0, 0, lift - neck_h / 2 - 14))

# pump: measured collar and body, made-up head. Its collar rests on the lips.
zc = hc.z_top
cd = dim("PUMP_C_COLLAR_DEPTH")
pump = (cylinder(dim("PUMP_C_COLLAR_OD") / 2, cd + 2, "z", (0, 0, zc + (cd + 2) / 2))
        + cylinder(dim("PUMP_C_BODY_OD") / 2, S["pump_body_len"], "z", (0, 0, zc - S["pump_body_len"] / 2 + 1))
        + cylinder(S["pump_stem_d"] / 2, S["pump_stem_h"], "z", (0, 0, zc + cd + 2 + S["pump_stem_h"] / 2))
        + cylinder(S["pump_head_d"] / 2, 7, "z", (0, 0, zc + cd + 2 + S["pump_stem_h"] + 3.5))
        + box(-6, 6, -S["spout_len"], 0, zc + cd + 2 + S["pump_stem_h"], zc + cd + 2 + S["pump_stem_h"] + 7))
pump -= cylinder(dim("PUMP_C_COLLAR_OD") / 2 - dim("PUMP_C_COLLAR_WALL"), cd, "z", (0, 0, zc + cd / 2)) - cylinder(dim("PUMP_C_BODY_OD") / 2, cd, "z", (0, 0, zc + cd / 2))

collar = hc.part


def scene(dz_pump=0, dz_bottle=0, dy_collar=0, cut=False):
    items = [(bracket, METAL), (bottle.translate((0, 0, dz_bottle)), GLASS),
             (collar.translate((0, dy_collar, 0)), PRINT), (pump.translate((0, 0, dz_pump)), PUMP)]
    if cut:   # keep the half behind the plane x = 0
        keep = box(0, 200, -200, 200, -300, 300)
        items = [(s & keep, g) for s, g in items]
    return items


VIEWS = {
    "preview": ("In place", scene(), View((-0.75, -1, 0.55)), 620),
    "view-below": ("From below", scene(), View((-0.8, -1, -0.5)), 620),
    "view-exploded": ("How it goes together", scene(dz_pump=55, dz_bottle=-40, dy_collar=-48), View((-0.9, -1, 0.5)), 620),
    "view-section": ("Cut in half", scene(cut=True), View((-1, -0.25, 0.12)), 380),
    "view-collar-top": ("The collar, from above", [(collar, PRINT)], View((-0.6, 1, 0.75)), 520),
    "view-collar-below": ("The collar, from below", [(collar, PRINT)], View((-0.7, -1, -0.7)), 520),
}
OUT.mkdir(exist_ok=True)
for name, (title, items, view, width) in VIEWS.items():
    body, (w, h) = render(items, view, width=width)
    pad, head = 24, 44
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w + 2 * pad:.0f}" height="{h + head + pad:.0f}">'
           f'<rect width="100%" height="100%" fill="#f6f7f8"/>'
           f'<text x="{pad}" y="29" font-family="Helvetica, Arial, sans-serif" font-size="18" font-weight="700" fill="#1c2226">{title}</text>'
           f'<g transform="translate({pad},{head})">{body}</g></svg>')
    tmp = OUT / f"{name}.svg"
    tmp.write_text(svg)
    subprocess.run(["rsvg-convert", "-z", "2", str(tmp), "-o", str(OUT / f"{name}.png")], check=True)
    tmp.unlink()
    print("wrote", OUT / f"{name}.png")
