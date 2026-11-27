"""Split-ring gauge: finds the bore for a ring that snaps over the amber neck's 44.0 thread and closes on the 43.5 neck.

Four short rings with the real ring's 5.5 wall and a slot through it; notches on the outside count 1-4, smallest bore
first. Pump off, push each over the thread onto the bare neck. Pick the smallest that goes on by hand and sits snug.

    uv run python cad/amber_split_gauge.py     # writes exports/amber_split_gauge.*
"""
from workshop.cad.checks import fits_bed, overhangs
from workshop.cad.export import export
from workshop.cad.geometry import box, cylinder

import amber_holder as ah

dim = ah.dim
h, slot, wall = dim("SPLIT_GAUGE_HEIGHT"), dim("SPLIT_SLOT"), dim("RING_WALL")
bores = sorted(dim("SPLIT_GAUGE_BORES"))
pitch = max(bores) + 2 * wall + 5

part = None
for i, d in enumerate(bores):
    ro, x, y = d / 2 + wall, (i % 2) * pitch, (i // 2) * pitch
    ring = cylinder(ro, h, "z", (x, y, h / 2)) - cylinder(d / 2, h + 2, "z", (x, y, h / 2))
    ring -= box(x - slot / 2, x + slot / 2, y - ro - 1, y - d / 2 + 1, -1, h + 1)       # the slot, at -y
    for n in range(i + 1):                                                               # count notches, at +x
        ny = y + (n - i / 2) * 3
        ring -= box(x + ro - 1, x + ro + 1, ny - 0.75, ny + 0.75, -1, h + 1)
    part = ring if part is None else part + ring

# thin ties on the bed hold the four together (one plate, one file); snap them off. Off-axis, clear of slots and notches
t, off = 0.6, 15.0
for (x0, y0), (x1, y1) in (((0, -off), (pitch, -off)), ((0, pitch - off), (pitch, pitch - off)), ((off, 0), (off, pitch))):
    a, b = (x0 + 20, x1 - 20) if y0 == y1 else (y0 + 20, y1 - 20)
    part += box(a, b, y0 - 1, y0 + 1, 0, t) if y0 == y1 else box(x0 - 1, x0 + 1, a, b, 0, t)

# opening the slot to pass the thread, as a C-ring: bending strain about t * gap / (4 pi R^2)
gap = 3.1416 * (dim("AMBER_NECK_THREAD_OD") - min(bores))
strain = wall * gap / (4 * 3.1416 * ((min(bores) / 2 + wall / 2) ** 2))
assert strain < 0.01, strain   # PLA yields around 2-3 %

if __name__ == "__main__":
    assert fits_bed(part, ah.BED)
    print(dict(bores=bores, od=[round(d + 2 * wall, 1) for d in bores], slot=slot, height=h,
               spread_strain_pct=round(100 * strain, 2), overhangs=overhangs(part)))
    export("amber_split_gauge", part, ah.OUT)
