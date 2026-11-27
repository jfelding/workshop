"""One-head Oral-B travel case: DrJones's two-head print-in-place case, cut down to one head.

    uv run python cad/single_case.py      # writes exports/{single_case,hinge_test}{,_widetol}.{stl,png}, preview.png

The original (vendor/oralbox2/, CC BY 4.0, see the README there) lies open on the bed as two halves joined by a
print-in-place hinge along X. Each half is two lanes wide, one per head. For one head:

- the far clip and both stand pegs are cut off at the floor. With one head on the centre line a peg would hit it,
  so the single case is a travel case only;
- each half loses one lane (15 mm) past the clip, where only the brush tube lies;
- from the end wall to just past the clip the full width stays, because the bristles point sideways into it. A copy
  of the far end wall closes the step.

The kept clip, the hinge, the latch and the finger slot are untouched, so the normal and wide-tolerance ("widetol")
files keep their hinge clearance. The source is a mesh, so the part is cut with trimesh and has no STEP file.
"""
import sys
from pathlib import Path

import numpy as np
import trimesh

from workshop.cad.preview import preview
from workshop.measure import dims

import measurements as m

dim = dims(m)
ROOT = Path(__file__).parents[1]
VENDOR = ROOT / "vendor" / "oralbox2"
OUT = ROOT / "exports"
SOURCES = {"single_case": VENDOR / "oralbox2.stl", "single_case_widetol": VENDOR / "oralbox2-widetol.3mf"}


def load(path):
    """The original as one mesh, without the zero-volume slivers the widetol 3MF carries."""
    mesh = trimesh.load(path, force="mesh")
    bodies = [b for b in mesh.split(only_watertight=False) if b.is_watertight and b.volume > 1.0]
    assert len(bodies) == 2, f"{path.name}: expected two halves, found {len(bodies)} solid bodies"
    return bodies


def keep(mesh, y, side):
    """The part of mesh on one side of the plane y = const (side +1: y >= y, side -1: y <= y), as a closed solid."""
    big = 1000.0
    box = trimesh.creation.box(extents=(big, big, big))
    box.apply_translation((0, y + side * big / 2, 0))
    return trimesh.boolean.intersection([mesh, box], engine="manifold")


def above_floor(box_xy):
    """A cutter over box_xy = ((x0, x1), (y0, y1)) from the floor's top face upward."""
    (x0, x1), (y0, y1) = box_xy
    z0, z1 = dim("FLOOR_TOP_Z"), 40.0
    cut = trimesh.creation.box(extents=(x1 - x0 + 1.0, y1 - y0 + 1.0, z1 - z0))
    cut.apply_translation(((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    return cut


def region(x=(-1e3, 1e3), y=(-1e3, 1e3)):
    """A box spanning x and y over every z, to intersect with."""
    (x0, x1), (y0, y1) = x, y
    box = trimesh.creation.box(extents=(x1 - x0, y1 - y0, 1e3))
    box.apply_translation(((x0 + x1) / 2, (y0 + y1) / 2, 0))
    return box


def cut(mesh, *boxes):
    """mesh intersected with the union of boxes."""
    keep = trimesh.boolean.union(boxes, engine="manifold") if len(boxes) > 1 else boxes[0]
    return trimesh.boolean.intersection([mesh, keep], engine="manifold")


def stepped(full, narrow_, side):
    """Full width up to the step wall, narrow after it. side = -1 for the cradle half (outer wall at -y), +1 stand.

    Pieces: the full half up to the end wall's corner line (x <= step inner face - fillet), the narrow half from the
    step wall's inner face on, and a slab of the far end wall moved to STEP_WALL_X, between the two outer walls.
    In the lane, where full and narrow are the same solid, the full piece runs OVERLAP past the step wall's inner face
    and the clip's end, so the join overlaps and no cut lies on an existing face.
    """
    L, slab, corner, ov = dim("LENGTH"), dim("END_WALL_SLAB"), dim("END_CORNER_X"), dim("OVERLAP")
    xs = dim("STEP_WALL_X")
    inner_face = xs - 2.0                                     # end wall is 2.0 thick (END_WALL_SLAB)
    lane_edge = side * (dim("INNER_WALL_Y") - dim("LANE_PITCH") + ov)   # 0.5 inside the narrow outer wall
    lane = (-1e3, lane_edge) if side > 0 else (lane_edge, 1e3)
    band = (lane_edge, 1e3) if side > 0 else (-1e3, lane_edge)
    lane_end = max(inner_face, dim("CRADLE_A_X")[1]) + ov     # past the clip's end face, never on it
    a = cut(full, region(x=(-1e3, xs - corner)), region(x=(-1e3, lane_end), y=lane))
    b = cut(narrow_, region(x=(inner_face, 1e3), y=band), region(x=(lane_end - ov / 2, 1e3), y=lane))
    wall = cut(full, region(x=(L - slab, 1e3), y=band))
    wall.apply_translation((xs - L, 0, 0))
    out = trimesh.boolean.union([a, b, wall], engine="manifold")
    assert out.is_watertight and len(out.split()) == 1, "the stepped half is not one closed solid"
    return out


def narrow(half, cut, toward_hinge):
    """Remove the strip cut = (y0, y1) from a half and slide the outer piece toward the hinge to close the gap."""
    y0, y1 = cut
    width = y1 - y0
    ov = dim("OVERLAP")
    if toward_hinge > 0:          # cradle half (y < 0): the outer piece is at y < y0 and moves +width
        inner, outer = keep(half, y1 - ov, +1), keep(half, y0, -1)
    else:                         # stand half (y > 0): the outer piece is at y > y1 and moves -width
        inner, outer = keep(half, y0 + ov, -1), keep(half, y1, +1)
    outer.apply_translation((0, toward_hinge * width, 0))
    out = trimesh.boolean.union([inner, outer], engine="manifold")
    assert out.is_watertight and len(out.split()) == 1, "the narrowed half is not one closed solid"
    return out


def build(src):
    cradle, stand = sorted(load(src), key=lambda b: b.bounds[0][1])
    cradle = cradle.difference(above_floor(dim("CRADLE_B_BOX")), engine="manifold")
    stand = stand.difference(above_floor(dim("PEG_BOX")), engine="manifold")
    w, wall = dim("LANE_PITCH"), dim("INNER_WALL_Y")
    c0 = -wall + 1.25                                         # in the flat floor, clear of the wall fillet
    assert c0 + w < dim("CRADLE_A_Y")[0] - dim("OVERLAP"), "the cut would reach the kept clip"
    assert dim("STAND_CUT_Y")[1] - dim("STAND_CUT_Y")[0] == w, "both halves must lose the same width"
    assert dim("STEP_WALL_X") - 2.0 >= dim("CRADLE_A_X")[1] - 0.5, "the step wall would cut into the clip"
    narrow_c = narrow(cradle, (c0, c0 + w), +1)
    narrow_s = narrow(stand, dim("STAND_CUT_Y"), -1)
    return stepped(cradle, narrow_c, -1), stepped(stand, narrow_s, +1)


def hinge_test(cradle, stand):
    """The first HINGE_TEST_LENGTH mm of the case along the hinge: end wall, three knuckles, both halves."""
    x = dim("HINGE_TEST_LENGTH")
    big = 1000.0
    box = trimesh.creation.box(extents=(big, big, big))
    box.apply_translation((x - big / 2, 0, 0))
    return [trimesh.boolean.intersection([h, box], engine="manifold") for h in (cradle, stand)]


def write(name, halves):
    part = trimesh.util.concatenate(halves)
    stl = OUT / f"{name}.stl"
    part.export(stl)
    preview(stl, OUT / f"{name}.png")
    print(f"{name}: {np.round(part.extents, 1).tolist()} mm, {sum(h.volume for h in halves) / 1000:.1f} cm³")


def main():
    OUT.mkdir(exist_ok=True)
    for name, src in SOURCES.items():
        halves = build(src)
        write(name, halves)
        write(name.replace("single_case", "hinge_test"), hinge_test(*halves))
    preview(OUT / "single_case.stl", OUT / "preview.png", px=700)


if __name__ == "__main__":
    sys.exit(main())
