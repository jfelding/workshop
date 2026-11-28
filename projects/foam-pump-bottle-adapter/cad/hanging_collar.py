"""Hanging collar (concept 6): a threaded collar under the bracket ring, hooked over the ring's edge.

It slides onto the ring from the front. The clear bottle screws up into it until the top of its neck
presses against the underside of the metal ring, which clamps everything. The pump then drops through
the bracket hole into the bottle and rests on the lips. Print as modelled: threaded end on the bed.

    uv run python cad/hanging_collar.py            # refuses until the ring's front is measured
    uv run python cad/hanging_collar.py --draft    # assumes a half-circle front, writes hanging_collar_draft
"""
import math
import sys
from pathlib import Path

from build123d import Axis, Circle, Helix, Plane, Polygon, Pos, Rectangle, chamfer, extrude, sweep

from workshop.cad.checks import fits_bed, overhangs, overlap, probe
from workshop.cad.export import export
from workshop.cad.geometry import box, cylinder
from workshop.fits import hole_for
from workshop.measure import dims

import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
BED = (220, 220, 270)   # Neptune 3 Pro
DRAFT = "--draft" in sys.argv

# z = 0 is the underside of the metal ring; +y points to the wall, -y to the front.
hole = dim("BRACKET_HOLE_DIAMETER")
ring_w = dim("BRACKET_RING_OUTER_WIDTH")
side_metal = (ring_w - hole) / 2
front_metal = side_metal if DRAFT else dim("BRACKET_RING_FRONT_WIDTH")
assert abs(front_metal - side_metal) < 0.5, "front is not a half circle around the hole: redesign the web"
t = dim("BRACKET_PLATE_THICKNESS")

L, wall, web = dim("COLLAR_LENGTH"), dim("COLLAR_WALL"), dim("COLLAR_WEB")
ri = ring_w / 2 + dim("COLLAR_RING_SIDE_PLAY")      # inside of the web
ro = ri + web
reach = dim("COLLAR_LIP_REACH")
rail = math.sqrt(ro ** 2 - (ri + dim("COLLAR_RAIL_MIN_WALL")) ** 2)   # how far back the lips run along the straight sides
assert rail < hole / 2, "lips would run past the flat metal we know about"
z_lip = t + dim("COLLAR_RING_LIFT") - (ri - ring_w / 2)   # where the 45° lip face meets the web
z_top = z_lip + reach + dim("COLLAR_LIP_TIP")

cav_r = hole_for(dim("WIDE_NECK_THREAD_OD"), "running") / 2   # the neck's thread crests pass this
tip_r = dim("WIDE_NECK_ROOT_OD") / 2 + dim("THREAD_TIP_CLEARANCE")
pitch = dim("WIDE_NECK_THREAD_PITCH")
assert cav_r + wall <= ro


def u_face(r, back):
    """Disc of radius r plus a strip of the same width running back to y = back: the ring's outline."""
    return Circle(r) + Pos(0, back / 2) * Rectangle(2 * r, back)


# body: threaded tube below the ring, web and lips above it at the front and sides
tube = extrude(Pos(0, 0, -L) * Circle(ro), L)   # the outside is one plain cylinder
tube = chamfer(tube.edges().group_by(Axis.Z)[0], dim("COLLAR_EDGE_CHAMFER"))
upper = extrude(Circle(ro), z_top) - box(-ro - 1, ro + 1, rail, ro + 1, -1, z_top + 1)
far = rail + 20   # the ring's keep-out runs on towards the wall
ring_void = (extrude(u_face(ri, far), z_lip)
             + extrude(Pos(0, 0, z_lip) * u_face(ri, far), reach, taper=45)
             + extrude(Pos(0, 0, z_lip + reach - 0.01) * u_face(ri - reach, far), z_top))
part = tube + (upper - ring_void)
part -= cylinder(cav_r, L + 2, "z", (0, 0, -L / 2))   # the neck's passage; cut bores last

# thread: one helical ridge inside. Lower flank 45° (prints unsupported), upper flank nearly flat (carries the bottle)
depth = cav_r - tip_r
tip_w, run = dim("THREAD_TIP_WIDTH"), dim("THREAD_BEARING_RUN")
ridge_h = depth + tip_w + run
assert ridge_h < pitch - 0.5, "ridge leaves no room for the neck's own thread"
z0 = -L + dim("THREAD_END_MARGIN")
helix_h = L - 2 * dim("THREAD_END_MARGIN") - ridge_h
embed = 0.3
profile = Plane.XZ * Pos(cav_r, 0) * Polygon(
    (embed, 0), (0, 0), (-depth, depth), (-depth, depth + tip_w), (0, ridge_h), (embed, ridge_h), align=None)
ridge = sweep(profile, Helix(pitch, helix_h, cav_r), is_frenet=True).translate((0, 0, z0))
part = part + ridge

# checks against the solid
neck_core = cylinder(dim("WIDE_NECK_ROOT_OD") / 2, 40, "z", (0, 0, -10))
ring = extrude(Pos(0, 0, dim("COLLAR_RING_LIFT")) * (u_face(ring_w / 2, far) - Circle(hole / 2)), t)
pump_body = cylinder(dim("PUMP_C_BODY_OD") / 2, 60, "z", (0, 0, 0))
for name, keepout in (("neck core", neck_core), ("ring, clamped", ring), ("pump body", pump_body)):
    v = overlap(part, keepout)
    print(f"overlap with {name}: {v:.2f} mm³")
    assert v < 0.01, name
z_mid = -L / 2
print(f"cavity Ø{2 * cav_r:.2f}, thread tip Ø{2 * tip_r:.2f}, ridge {depth:.2f} deep × {ridge_h:.2f} tall, "
      f"{helix_h / pitch:.1f} turns at pitch {pitch}")
print(f"wall at the back {probe(part, (0, cav_r + 0.05, -L + 0.7), (0, 40, -L + 0.7)):.2f} mm, "
      f"web at the front {probe(part, (0, -ri - 0.05, 0.5), (0, -40, 0.5)):.2f} mm, "
      f"lip top {z_top:.2f} mm above the ring's underside, outer width {2 * ro:.1f} mm")

printed = part.translate((0, 0, L))   # threaded end on the bed
assert fits_bed(printed, BED)
print("overhangs", overhangs(printed))
if __name__ == "__main__":
    export("hanging_collar_draft" if DRAFT else "hanging_collar", printed, OUT)
