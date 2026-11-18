"""Bose half of the adapter: Dr. Watt's earpad frame with two pin pockets cut into its flat back.

    uv run python cad/bose_half.py         # writes exports/bose_half.{stl,png}

The frame (vendor/bose-earpad-frame/, CC BY-NC-SA, see the README there) is the part that clips
into the Bose earcup. It is used unchanged apart from two blind pockets on the flat side, which
take the alignment pins. The clip side is untouched.

Both halves are modelled glue face down at z = 0. To glue them the frame is turned over about
its long (Y) axis, which maps x to -x, so its pockets sit at the mirror image of the Dyson
half's pin holes. The source is a mesh, so this part is cut with trimesh and has no STEP file.
"""
from pathlib import Path

import numpy as np
import trimesh

from workshop.cad.preview import preview
from workshop.measure import dims

import measurements as m
from dyson_half import pin_positions

dim = dims(m)
ROOT = Path(__file__).parents[1]
FRAME = ROOT / "vendor" / "bose-earpad-frame" / "frame_body1.stl"
OUT = ROOT / "exports"
NAME = "bose_half"


def pocket(x, y):
    """Blind pocket cutter at (x, y): chamfered mouth at z = 0, flat roof."""
    r, c, depth = dim("PIN_PRESS_POCKET") / 2, dim("PIN_HOLE_CHAMFER"), dim("PIN_POCKET_DEPTH")
    profile = np.array([(0, -1), (r + c + 1, -1), (r, c), (r, depth), (0, depth)])   # (radius, z)
    cut = trimesh.creation.revolve(profile, sections=48)
    cut.apply_translation((x, y, 0))
    return cut


def make():
    frame = trimesh.load(FRAME)
    size = frame.extents
    assert abs(frame.bounds[0][2]) < 1e-6, "flat back expected at z = 0"
    assert abs(size[0] - dim("BOSE_OVAL_X")) < 0.1 and abs(size[1] - dim("BOSE_OVAL_Y")) < 0.1, size
    for x, y in pin_positions():
        frame = frame.difference(pocket(-x, y), engine="manifold")
    return frame


if __name__ == "__main__":
    part = make()
    assert part.is_watertight and len(part.split()) == 1
    OUT.mkdir(exist_ok=True)
    part.export(OUT / f"{NAME}.stl")
    x, y, z = part.extents
    print(f"{NAME}: {x:.1f} × {y:.1f} × {z:.1f} mm, {part.volume / 1000:.1f} cm³ → {OUT / NAME}.stl")
    preview(OUT / f"{NAME}.stl")
