"""Bose half with a wide rim, to glue to dyson_half_wide so the pair has a flush edge all round.

    uv run python cad/bose_half_wide.py        # writes exports/bose_half_wide.{stl,png}

UNTESTED. It is bose_half (Dr. Watt's frame, CC BY-NC-SA, plus the two mirrored pin pockets) with extra material
added only OUTSIDE the frame's oval: the ring between the oval and the wide outline of dyson_half_wide (the same
outline() function, so COVER_RADIUS and OUTLINE_BLEND_RADIUS cannot drift apart between the halves). The rim is
a flat plate at the frame's own plate thickness (z = 0 glue face to z = BOSE_FRAME_THICKNESS), 0.4 mm of it
overlapping the frame's plate so the union is clean. The frame's outer wall is vertical and sharp (read from the
mesh), so the rim has a 0.3 mm chamfer on both outer edges, like the Dyson half's; nothing inside the frame's
outline is changed. Glue face down, flat, no support. Mesh edit, so no STEP file.
"""
import tempfile
from pathlib import Path

import trimesh
from build123d import Ellipse, chamfer, export_stl, extrude

from workshop.cad.preview import preview
from workshop.measure import dims

import bose_half
import dyson_half_wide
import measurements as m

dim = dims(m)
OUT = bose_half.OUT
NAME = "bose_half_wide"
OVERLAP = 0.4      # how far the rim reaches inside the frame's oval, into its solid plate


def rim_solid():
    """The ring between (oval - OVERLAP) and the wide outline, as a build123d solid with chamfered outer edges."""
    a, b = dim("BOSE_OVAL_X") / 2, dim("BOSE_OVAL_Y") / 2
    t = dim("BOSE_FRAME_THICKNESS")
    rim = extrude(dyson_half_wide.outline() - Ellipse(a - OVERLAP, b - OVERLAP), t)
    outer = lambda z: rim.edges().filter_by(lambda e: abs(e.center().Z - z) < 1e-3 and
                                            (e.position_at(0.5).X / (a - 0.2)) ** 2 +
                                            (e.position_at(0.5).Y / (b - 0.2)) ** 2 > 1)
    rim = chamfer(outer(0), dim("BACK_EDGE_CHAMFER"))
    return chamfer(outer(t), dim("BACK_EDGE_CHAMFER"))


def make():
    frame = bose_half.make()                       # the proven part: frame plus the two pin pockets
    with tempfile.TemporaryDirectory() as tmp:
        export_stl(rim_solid(), Path(tmp) / "rim.stl", tolerance=0.01, angular_tolerance=0.1)
        rim = trimesh.load(Path(tmp) / "rim.stl")
    return trimesh.boolean.union([frame, rim], engine="manifold")


if __name__ == "__main__":
    part = make()
    assert part.is_watertight and len(part.split()) == 1
    OUT.mkdir(exist_ok=True)
    part.export(OUT / f"{NAME}.stl")
    x, y, z = part.extents
    print(f"{NAME}: {x:.1f} × {y:.1f} × {z:.1f} mm, {part.volume / 1000:.1f} cm³ → {OUT / NAME}.stl")
    preview(OUT / f"{NAME}.stl")
