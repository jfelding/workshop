"""Bose half for the latch variant: bose_half_wide with a relief pocket under each spring arm.

    uv run python cad/bose_half_latch.py       # writes exports/bose_half_latch.{stl,png}

UNTESTED. dyson_half_latch has two flexure arms that bend down past the glue face when the cushion's face
presses their teeth flat. This part gives each arm a blind pocket to bend into (BOSE_LATCH_POCKET_DEPTH deep, so
0.4 mm of the 2.0 mm plate stays closed towards the earcup) and keeps the superglue line away from the arm:
the pocket is a little larger than the arm and its slits, and fits either pawl, so the halves glue either way round. Positions come from dyson_half_latch.pawls(), mirrored
(the halves glue back to back, x to -x), so the two parts cannot drift apart. Glue face down, no support; the
pocket roof is a 5 mm bridge. Remix of Dr. Watt's frame (CC BY-NC-SA). Mesh edit, so no STEP file.
"""
import tempfile
from pathlib import Path

import trimesh
from build123d import export_stl

from workshop.cad.preview import preview
from workshop.measure import dims

import bose_half_wide
import dyson_half_latch as dl
import measurements as m

dim = dims(m)
OUT = bose_half_wide.OUT
NAME = "bose_half_latch"


def pocket_spans():
    """Each pocket in THIS part's frame (angles mirrored: a -> 180 - a), as two sectors [(r0, r1, a0, a1)].

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
        # The pins let the halves go together either way round, and the teeth are staggered, so each pocket
        # also covers the other pawl turned half a turn.
        turn = 180 - 360 * round((own[1 - i][0] + 180 - mine[0]) / 360)
        other = [a + turn for a in own[1 - i]]
        a0, step, a1 = min(mine[0], other[0]), min(mine[1], other[1]), max(mine[2], other[2])
        out.append([(dl.R_TIP - clear, r1, a0, step + 0.05), (dl.R_IN - dl.SLIT - mg, r1, step, a1)])
    return out


def pocket_mesh(r0, r1, a0, a1, z0, z1):
    with tempfile.TemporaryDirectory() as tmp:
        export_stl(dl.sector(r0, r1, a0, a1, z0, z1), Path(tmp) / "p.stl", tolerance=0.01, angular_tolerance=0.1)
        return trimesh.load(Path(tmp) / "p.stl")


def make():
    part = bose_half_wide.make()
    for pocket in pocket_spans():
        for r0, r1, a0, a1 in pocket:
            part = part.difference(pocket_mesh(r0, r1, a0, a1, -1, dim("BOSE_LATCH_POCKET_DEPTH")), engine="manifold")
    return part


if __name__ == "__main__":
    part = make()
    assert part.is_watertight and len(part.split()) == 1
    OUT.mkdir(exist_ok=True)
    part.export(OUT / f"{NAME}.stl")
    x, y, z = part.extents
    print(f"{NAME}: {x:.1f} × {y:.1f} × {z:.1f} mm, {part.volume / 1000:.1f} cm³ → {OUT / NAME}.stl")
    preview(OUT / f"{NAME}.stl")
