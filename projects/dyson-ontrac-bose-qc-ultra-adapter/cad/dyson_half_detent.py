"""TEST VARIANT of the Dyson half with a click detent: two low ramped bumps on the relief step.

    uv run python cad/dyson_half_detent.py     # writes exports/dyson_half_detent.{stl,step,png}

UNTESTED, and built from photo-read ledge-bar positions (see measurements.py). It is
dyson_half.make() unchanged plus one bump on the relief surface in the path of each LONG ledge bar
(a 180-degree symmetric pair, so one part still serves both ears). The proven part is not touched.

Each cushion's ledge bar rides over the relief, 0.2 mm above it when the cushion is fully seated.
A bump 0.4 mm high is in the way of the bar: it must lift the cushion about 0.2 mm (the wedge hook lets
it, a little, away from home) or flex. The bar climbs the gentle approach side, crosses the crest, and
drops off the steeper release side; going back it has to climb the release side. The bars are about
as long as the twist travel, so they sit on the bump at drop-on too: see detent_check.py.
"""
import math
from pathlib import Path

from build123d import Align, Box, Cylinder, Face, Pos, Rot, Wire, extrude

from workshop.cad.checks import fits_bed
from workshop.cad.export import export
from workshop.measure import dims

import dyson_half
import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
NAME = "dyson_half_detent"
T_PLATE = dim("PLATE_THICKNESS")
Z_RELIEF = T_PLATE - dim("RELIEF_DEPTH")     # top of the stepped-down plate, where the bar passes


def bars_cad():
    """Ledge bars as they sit when the cushion is home, in the plate's (CAD) frame.

    Returns [(kind, lo, hi, r_in, r_out)]: angles in degrees, the bar spanning lo..hi. `hi` is the bar's
    closed (lock) end, which trails when the cushion twists home; `lo` leads. The plate frame is the
    mirror of the cushion-back view, turned by CUSHION_CLOCKING_DEG, as for the hooks.
    """
    clock = dim("CUSHION_CLOCKING_DEG")
    out = []
    for kind, a0, a1, r0, r1 in dim("LEDGE_BARS_PHOTO"):
        s0, s1 = a0 - dim("PHOTO_FRAME_OFFSET_DEG"), a1 - dim("PHOTO_FRAME_OFFSET_DEG")
        out.append([kind, clock - s1, clock - s0, r0, r1])
    return out


def long_bar():
    """The two long bars, averaged into one by turning the second through 180 degrees (symmetry)."""
    longs = [b for b in bars_cad() if b[0] == "long"]
    lo = (longs[0][1] + longs[1][1] - 180) / 2
    hi = (longs[0][2] + longs[1][2] - 180) / 2
    return lo, hi, max(b[3] for b in longs), min(b[4] for b in longs)


def bump_crest_deg():
    """Crest angle of the bump: the bar's trailing end is CREST_BEFORE_HOME_DEG short of home there."""
    return long_bar()[1] + dim("CREST_BEFORE_HOME_DEG")


def bump_profile():
    """(tangent offset mm, height mm) polygon of the bump, crest centred on 0; + is towards drop-on."""
    h, c = dim("BUMP_HEIGHT"), dim("BUMP_CREST_LENGTH")
    rel = h / math.tan(math.radians(dim("BUMP_RELEASE_DEG")))
    app = h / math.tan(math.radians(dim("BUMP_APPROACH_DEG")))
    return [(-c / 2 - rel, 0.0), (-c / 2, h), (c / 2, h), (c / 2 + app, 0.0)], rel, app


def bump(angle_deg):
    """One bump with its crest at `angle_deg`, standing on the relief surface."""
    r_in, r_out = dim("BUMP_INNER_RADIUS"), dim("BUMP_OUTER_RADIUS")
    prof, _, _ = bump_profile()
    sink = 0.1                                   # base sunk into the plate so the union fuses
    pts = [(r_in - 0.3, t, Z_RELIEF + z - (sink if z == 0 else 0)) for t, z in prof]
    # prism along the radius at angle 0, tangent = +y, then trimmed to the annulus and turned into place
    pts = [(0, t, z) for _, t, z in pts]
    face = Face(Wire.make_polygon(pts, close=True))
    prism = Pos(r_in - 0.3, 0, 0) * extrude(face, r_out - r_in + 0.6, dir=(1, 0, 0))
    ring = (Cylinder(r_out, 5, align=(Align.CENTER, Align.CENTER, Align.MIN))
            - Cylinder(r_in, 5, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return Rot(0, 0, angle_deg) * (prism & ring)


def make():
    part = dyson_half.make()
    c = bump_crest_deg()
    for a in (c, c + 180):
        part += bump(a)
    return part


if __name__ == "__main__":
    part = make()
    assert fits_bed(part, dyson_half.BED)
    prof, rel, app = bump_profile()
    print(f"long bar (home) {long_bar()}, crest at {bump_crest_deg():.2f} deg, ramps: release {rel:.2f} mm, "
          f"approach {app:.2f} mm")
    export(NAME, part, OUT, tolerance=0.01, angular_tolerance=0.1)
