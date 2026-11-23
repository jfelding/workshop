"""TEST VARIANT of the WIDE Dyson half with a spring latch: a pawl that clicks into each short slot.

    uv run python cad/dyson_half_latch.py      # writes exports/dyson_half_latch.{stl,step,png}

UNTESTED. It is dyson_half_wide.make() with two flexure arms cut out of the seat by a U-shaped slit, one
beside each SHORT hook, each carrying a tooth on its free end. The tooth stands LATCH_TOOTH_HEIGHT above the
seat. The cushion's solid face presses it flat at drop-on; when the cushion is twisted home, the open end
of the short slot arrives over the tooth and it springs up behind the slot's end wall. To take the cushion off,
twist back: the wall rides up the tooth's sloped face and pushes the arm down. The arm bends into a pocket in
bose_half_latch, so this part glues to that one only. The proven parts are not touched.

The two teeth sit at slightly different places (LATCH_FOOT_BEHIND_WALL_DEG), so the part is no longer exactly
180-degree symmetric; it still serves both ears, because each cushion meets one of each.
"""
import math
from pathlib import Path

from build123d import Align, Circle, Cylinder, Face, Pos, Rot, Wire, extrude

from workshop.cad.checks import fits_bed
from workshop.cad.export import export
from workshop.measure import dims

import dyson_half
import dyson_half_wide
import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
NAME = "dyson_half_latch"
T_PLATE = dim("PLATE_THICKNESS")                            # seat top = the cushion's face when seated
Z_ARM = T_PLATE - dim("LATCH_ARM_TOP_BELOW_SEAT")           # arm top
R_IN, R_OUT, SLIT = dim("LATCH_ARM_INNER_RADIUS"), dim("LATCH_ARM_OUTER_RADIUS"), dim("LATCH_SLIT_WIDTH")
R_TIP = dim("LATCH_TOOTH_INNER_RADIUS")                     # inner radius of the narrow tip and the tooth
R_MID = (R_IN + R_OUT) / 2
DEG_PER_MM = math.degrees(1 / R_MID)
SLOT_INNER_RADIUS = dim("SLOT_OPPOSING_SPAN") / 2 - dim("SLOT_WIDE_WIDTH")


def short_slots():
    """[(open-end wall, closed end)] of each short slot with the cushion home, plate-frame degrees."""
    half = math.degrees(math.asin(dim("SLOT_SHORT_CHORD") / (2 * dyson_half.SLOT_PITCH_RADIUS)))
    return [(-c + dim("CUSHION_CLOCKING_DEG") - half, -c + dim("CUSHION_CLOCKING_DEG") + half)
            for c, kind in dim("SLOT_ANGLES") if kind == "short"]


def tooth_profile():
    """(tangent mm, z mm) of the tooth; 0 = foot of the lock face, + = towards the hook (the arm's tip)."""
    h = T_PLATE + dim("LATCH_TOOTH_HEIGHT") - Z_ARM
    run = h / math.tan(math.radians(dim("LATCH_LOCK_FACE_DEG")))
    back = h / math.tan(math.radians(dim("LATCH_BACK_FACE_DEG")))
    c = dim("LATCH_TOOTH_CREST")
    return [(0.0, Z_ARM), (run, Z_ARM + h), (run + c, Z_ARM + h), (run + c + back, Z_ARM)]


def pawls():
    """Each pawl's angles (plate-frame degrees). The arm runs from `root` up to `tip`; the slit ends at `slit_end`."""
    prof = tooth_profile()
    out = []
    for (wall, closed), behind in zip(short_slots(), dim("LATCH_FOOT_BEHIND_WALL_DEG")):
        foot = wall - behind
        tip = foot + (prof[-1][0] + 0.1) * DEG_PER_MM
        out.append({"wall": wall, "closed": closed, "foot": foot,
                    "narrow_from": foot - dim("LATCH_NARROW_BEFORE_FOOT") * DEG_PER_MM,
                    "crest": (foot + prof[1][0] * DEG_PER_MM, foot + prof[2][0] * DEG_PER_MM),
                    "tip": tip, "slit_end": tip + SLIT * DEG_PER_MM, "root": foot - dim("LATCH_ARM_LENGTH_DEG"),
                    "lowered_from": foot - dim("LATCH_ARM_LENGTH_DEG") - dim("LATCH_LOWER_PAST_ROOT") * DEG_PER_MM})
    return out


def sector(r0, r1, a0, a1, z0, z1):
    """Solid annular sector r0..r1, a0..a1 degrees (under 90 apart), z0..z1."""
    low = (Align.CENTER, Align.CENTER, Align.MIN)
    ring = Cylinder(r1, z1 - z0, align=low) - Cylinder(r0, z1 - z0, align=low)
    fan = Face(Wire.make_polygon([(0, 0, 0), dyson_half.polar(200, a0), dyson_half.polar(200, a1)], close=True))
    return Pos(0, 0, z0) * (ring & extrude(fan, z1 - z0))


def tooth(foot_deg):
    """The tooth with its lock-face foot on the radial line at `foot_deg`, sunk 0.1 into the arm so it fuses."""
    prof = tooth_profile()
    pts = [(0, prof[0][0], Z_ARM - 0.1)] + [(0, t, z) for t, z in prof] + [(0, prof[-1][0], Z_ARM - 0.1)]
    prism = Pos(R_TIP - 0.3, 0, 0) * extrude(Face(Wire.make_polygon(pts, close=True)), R_OUT - R_TIP + 0.6, dir=(1, 0, 0))
    return Rot(0, 0, foot_deg) * prism & sector(R_TIP, R_OUT, foot_deg - 5, foot_deg + 15, 0, 10)


def make():
    part = dyson_half_wide.make()
    low = (Align.CENTER, Align.CENTER, Align.MIN)
    for p in pawls():
        # the top of the arm (and a little of the seat past its root) comes down, so only the tooth touches
        part -= sector(R_IN - SLIT, R_OUT + SLIT, p["lowered_from"], p["slit_end"], Z_ARM, T_PLATE + 1)
        # the U-shaped slit, through the plate: both sides and round the tip; round ends at the root
        part -= (sector(R_IN - SLIT, R_OUT + SLIT, p["root"], p["slit_end"], -1, T_PLATE + 1)
                 - sector(R_IN, R_OUT, p["root"] - 1, p["tip"], -2, T_PLATE + 2))
        part -= sector(R_IN - SLIT / 2, R_TIP, p["narrow_from"], p["slit_end"], -1, T_PLATE + 1)   # the narrow tip
        for r in (R_IN - SLIT / 2, R_OUT + SLIT / 2):
            x, y, _ = dyson_half.polar(r, p["root"])
            part -= Pos(x, y, -1) * Cylinder(SLIT / 2, T_PLATE + 2, align=low)
        part += tooth(p["foot"])
    return part


if __name__ == "__main__":
    part = make()
    assert fits_bed(part, dyson_half.BED)
    assert len(part.solids()) == 1
    for p in pawls():
        print({k: (tuple(round(x, 2) for x in v) if isinstance(v, tuple) else round(v, 2)) for k, v in p.items()})
    export(NAME, part, OUT, tolerance=0.01, angular_tolerance=0.1)
