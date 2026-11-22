"""TEST VARIANT: the Dyson half with a wider outline, so it covers the cushion's hard back ring at the sides.

    uv run python cad/dyson_half_wide.py        # writes exports/dyson_half_wide.{stl,step,png}

UNTESTED, and the ring radius is read from a photo (measurements.py). The hooks, seat, pin holes and edge
treatment are those of dyson_half; only the outline changes: the Bose oval united with a circle of COVER_RADIUS
and blended with a large fillet. The bulge overhangs the Bose half at the left and right (180-degree symmetric,
one part for both ears). The relief step covers the whole plate outside the seat, so the proud ledge bars
still pass over the bulge. dyson_half.py is not touched.
"""
from pathlib import Path

from build123d import Axis, Circle, Ellipse, Pos, chamfer, extrude, fillet

from workshop.cad.checks import fits_bed
from workshop.cad.export import export
from workshop.measure import dims

import dyson_half as dh
import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
NAME = "dyson_half_wide"


def outline():
    """The wide outline as a 2D face: Bose oval + circle of COVER_RADIUS, corners blended."""
    union = Ellipse(dim("BOSE_OVAL_X") / 2, dim("BOSE_OVAL_Y") / 2) + Circle(dim("COVER_RADIUS"))
    return fillet(union.vertices(), dim("OUTLINE_BLEND_RADIUS"))


def make():
    t = dim("PLATE_THICKNESS")
    low = t - dim("RELIEF_DEPTH")
    bore = Circle(dim("BORE_DIAMETER") / 2)
    plate = extrude(outline() - bore, low)

    def rim(z):   # the outer edges at height z (the bore's edges are all inside 35 mm)
        return plate.edges().filter_by(lambda e: abs(e.center().Z - z) < 1e-3 and
                                       (e.position_at(0.5).X ** 2 + e.position_at(0.5).Y ** 2) ** 0.5 > 35)
    plate = chamfer(rim(0), dim("BACK_EDGE_CHAMFER"))
    plate = fillet(rim(low), dim("FRONT_EDGE_FILLET"))
    seat = extrude(Circle(dh.STEM_OUT) - bore, t)
    seat = fillet(seat.edges().filter_by(dh.GeomType.CIRCLE).group_by(Axis.Z)[-1].sort_by(lambda e: e.radius)[0],
                  dim("BORE_EDGE_FILLET"))
    part = plate + seat
    for x, y in dh.pin_positions():
        part -= dh.pin_hole(x, y)
    for start, span, kind in dh.hook_spans():
        part += Pos(0, 0, t) * dh.hook(start, span, kind)
    return part


if __name__ == "__main__":
    part = make()
    assert fits_bed(part, dh.BED)
    size = part.bounding_box().size
    assert abs(size.Y - dim("BOSE_OVAL_Y")) < 0.01
    print(f"wide plate {size.X:.2f} x {size.Y:.2f}")
    export(NAME, part, OUT, tolerance=0.01, angular_tolerance=0.1)
