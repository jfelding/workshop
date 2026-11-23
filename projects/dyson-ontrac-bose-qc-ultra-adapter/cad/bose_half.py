"""Bose half of the adapter: Dr. Watt's earpad frame with pin pockets, a wider rim and two latch pockets.

    uv run python cad/bose_half.py         # writes exports/bose_half.{stl,png}

The frame (vendor/bose-earpad-frame/, CC BY-NC-SA, see the README there) is the part that clips into the Bose
earcup. Its clip side is untouched. Three things are added on its flat back:

- two blind pockets for the alignment pins;
- a flat rim outside the frame's oval, out to the Dyson half's outline (the same outline() function, so the two
  cannot drift apart), at the frame's plate thickness, chamfered 0.3 like the Dyson half;
- a blind pocket under each of the Dyson half's spring arms (BOSE_LATCH_POCKET_DEPTH deep, so 0.4 mm of the
  2.0 mm plate stays closed towards the earcup). Each pocket fits either arm, so the halves glue either way round.

Both halves are modelled glue face down at z = 0. To glue them the frame is turned over about its long (Y) axis,
which maps x to -x, so its pockets sit at the mirror image of the Dyson half's. The source is a mesh, so this
part is cut with trimesh and has no STEP file. Glue face down, no support; the pocket roofs are short bridges.
"""
import tempfile
from pathlib import Path

import numpy as np
import trimesh
from build123d import Ellipse, chamfer, export_stl, extrude

from workshop.cad.preview import preview
from workshop.measure import dims

import dyson_half as dl
import measurements as m
from hooks import pin_positions

dim = dims(m)
ROOT = Path(__file__).parents[1]
FRAME = ROOT / "vendor" / "bose-earpad-frame" / "frame_body1.stl"
OUT = ROOT / "exports"
NAME = "bose_half"
OVERLAP = 0.4      # how far the rim reaches inside the frame's oval, into its solid plate


def pin_pocket(x, y):
    """Blind pocket cutter at (x, y): chamfered mouth at z = 0, flat roof."""
    r, c, depth = dim("PIN_PRESS_POCKET") / 2, dim("PIN_HOLE_CHAMFER"), dim("PIN_POCKET_DEPTH")
    profile = np.array([(0, -1), (r + c + 1, -1), (r, c), (r, depth), (0, depth)])   # (radius, z)
    cut = trimesh.creation.revolve(profile, sections=48)
    cut.apply_translation((x, y, 0))
    return cut


def to_mesh(solid):
    with tempfile.TemporaryDirectory() as tmp:
        export_stl(solid, Path(tmp) / "s.stl", tolerance=0.01, angular_tolerance=0.1)
        return trimesh.load(Path(tmp) / "s.stl")


def rim_solid():
    """The ring between (oval - OVERLAP) and the Dyson half's outline, with chamfered outer edges."""
    a, b = dim("BOSE_OVAL_X") / 2, dim("BOSE_OVAL_Y") / 2
    t = dim("BOSE_FRAME_THICKNESS")
    rim = extrude(dl.outline() - Ellipse(a - OVERLAP, b - OVERLAP), t)
    outer = lambda z: rim.edges().filter_by(lambda e: abs(e.center().Z - z) < 1e-3 and
                                            (e.position_at(0.5).X / (a - 0.2)) ** 2 +
                                            (e.position_at(0.5).Y / (b - 0.2)) ** 2 > 1)
    rim = chamfer(outer(0), dim("BACK_EDGE_CHAMFER"))
    return chamfer(outer(t), dim("BACK_EDGE_CHAMFER"))


def pocket_spans():
    """Each latch pocket in THIS part's frame (angles mirrored: a -> 180 - a), as two sectors [(r0, r1, a0, a1)].

    The first is under the arm's narrow tip and tooth, and starts outside the frame's clip; the second, full
    width, is under the rest of the arm and its slits.
    """
    mg, end = dim("BOSE_LATCH_POCKET_MARGIN"), dim("BOSE_LATCH_POCKET_END_MARGIN") * dl.DEG_PER_MM
    clear = dim("BOSE_LATCH_POCKET_TIP_CLEARANCE")
    r1 = dl.R_OUT + dl.SLIT + mg
    own = [(180 - (p["slit_end"] + end), 180 - (p["narrow_from"] + clear * dl.DEG_PER_MM), 180 - (p["root"] - end))
           for p in dl.pawls()]
    out = []
    for i, mine in enumerate(own):
        # The pins let the halves go together either way round, so each pocket also covers the other pawl
        # turned half a turn (identical while both teeth sit at the same LATCH_FOOT_BEHIND_WALL_DEG).
        turn = 180 - 360 * round((own[1 - i][0] + 180 - mine[0]) / 360)
        other = [a + turn for a in own[1 - i]]
        a0, step, a1 = min(mine[0], other[0]), min(mine[1], other[1]), max(mine[2], other[2])
        out.append([(dl.R_TIP - clear, r1, a0, step + 0.05), (dl.R_IN - dl.SLIT - mg, r1, step, a1)])
    return out


def before_pockets():
    """Frame + pin pockets + rim: everything but the latch pockets (latch_check compares against it)."""
    frame = trimesh.load(FRAME)
    size = frame.extents
    assert abs(frame.bounds[0][2]) < 1e-6, "flat back expected at z = 0"
    assert abs(size[0] - dim("BOSE_OVAL_X")) < 0.1 and abs(size[1] - dim("BOSE_OVAL_Y")) < 0.1, size
    for x, y in pin_positions():
        frame = frame.difference(pin_pocket(-x, y), engine="manifold")
    return trimesh.boolean.union([frame, to_mesh(rim_solid())], engine="manifold")


def make():
    part = before_pockets()
    for pocket in pocket_spans():
        for r0, r1, a0, a1 in pocket:
            cut = to_mesh(dl.sector(r0, r1, a0, a1, -1, dim("BOSE_LATCH_POCKET_DEPTH")))
            part = part.difference(cut, engine="manifold")
    return part


if __name__ == "__main__":
    part = make()
    assert part.is_watertight and len(part.split()) == 1
    OUT.mkdir(exist_ok=True)
    part.export(OUT / f"{NAME}.stl")
    x, y, z = part.extents
    print(f"{NAME}: {x:.1f} × {y:.1f} × {z:.1f} mm, {part.volume / 1000:.1f} cm³ → {OUT / NAME}.stl")
    preview(OUT / f"{NAME}.stl")
