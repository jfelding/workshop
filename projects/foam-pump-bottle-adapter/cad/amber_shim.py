"""Quick fix for the printed ring v4: a 2 mm shim that goes on the neck before it and sits under it.

v4 (4.5 tall) let the bottle lift 2.0 mm before the shoulder caught it. Ring v5 (amber_holder.py) is 2 mm taller and
its bore hugs the shoulder. This shim is v5's bottom 2 mm as a separate ring, so v4 + shim is v5 below v4's underside
(less the web, which v4 already has above). It is loose: the shoulder pushes it up against v4's flat underside. Its
bore is the same cutter as v5's, so amber_checks.py's clash and lift checks on v5 cover it.

    uv run python cad/amber_shim.py     # writes exports/amber_ring_shim.*
"""
from build123d import Axis

from workshop.cad.checks import fits_bed, overhangs
from workshop.cad.export import export
from workshop.cad.geometry import cylinder

import amber_holder as ah

dim = ah.dim
z1 = ah.ring_z1 - dim("RING_V4_THICKNESS")   # v4's underside
z0 = ah.ring_z0                              # v5's underside
assert z1 - z0 > 0.5, "nothing to shim: v5 is not taller than v4"
shim = cylinder(ah.ring_ro, z1 - z0, "z", (0, 0, (z0 + z1) / 2)) - ah.bore_cutter()
wall = ah.ring_ro - ah.bore_r(z0)
assert wall >= 1.6, wall   # 4 perimeters at its thin bottom edge

# printed upside down: the flat top on the bed, the bore widening away from it
shim_print = shim.rotate(Axis.X, 180)
shim_print = shim_print.translate((0, 0, -shim_print.bounding_box().min.Z))

if __name__ == "__main__":
    assert fits_bed(shim_print, ah.BED)
    print("amber_ring_shim overhangs", overhangs(shim_print))
    print(dict(height=round(z1 - z0, 2), od=round(2 * ah.ring_ro, 2), bore_top=round(2 * ah.bore_r(z1), 2),
               bore_bottom=round(2 * ah.bore_r(z0), 2), wall_bottom=round(wall, 2), volume_cm3=round(shim.volume / 1000, 2)))
    export("amber_ring_shim", shim_print, ah.OUT)
