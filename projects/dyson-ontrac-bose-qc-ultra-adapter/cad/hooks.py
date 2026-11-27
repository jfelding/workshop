"""The twist-lock geometry shared by both halves: the hooks, the pins, and where they sit.

Measured and tuned by twelve test prints of the first, narrow version (v1). The hooks are unchanged since:
each is a stem with an outward lip whose gap to the seat narrows along its length (a wedge), so twisting the
cushion draws it down onto the seat and clamps it. The hook pattern is 180-degree symmetric and the left and
right cushions are identical, so one part serves both ears. dyson_half.py builds the plate around them.
"""
import math
from pathlib import Path

from build123d import Align, Cone, Cylinder, Face, Pos, Solid, Wire, extrude

from workshop.measure import dims

import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
BED = (220, 220, 270)   # Neptune 3 Pro, from equipment/neptune-3-pro

STEM_OUT = dim("STEM_OUTER_RADIUS")
HOOK_H = dim("HOOK_HEIGHT")
# Centre line of the slots: half the span across two opposite slots, less half a slot width.
SLOT_PITCH_RADIUS = (dim("SLOT_OPPOSING_SPAN") - dim("SLOT_WIDE_WIDTH")) / 2


def polar(r, deg, z=0.0):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a), z)


def ellipse_radius(a, b, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return 1 / math.sqrt((c / a) ** 2 + (s / b) ** 2)


def pin_positions():
    """(x, y) of each pin: midway across the glue band, from the Bose opening to the outline."""
    out = []
    for ang in dim("PIN_ANGLES_DEG"):
        r = (ellipse_radius(dim("BOSE_OPENING_X") / 2, dim("BOSE_OPENING_Y") / 2, ang)
             + ellipse_radius(dim("BOSE_OVAL_X") / 2, dim("BOSE_OVAL_Y") / 2, ang)) / 2
        out.append(polar(r, ang)[:2])
    return out


def hook_profile(gap, kind):
    """(r, z) outline of a hook's cross-section; z = 0 is the seat, `gap` the height under the lip."""
    r_in, lip, flat = dim("STEM_INNER_RADIUS")[kind], dim("LIP_OUTER_RADIUS")[kind], dim("LIP_FLAT_FROM_RADIUS")
    tip = dim("HOOK_TIP_CHAMFER")
    slope = math.tan(math.radians(dim("LIP_UNDERSIDE_SLOPE_DEG")))
    return [(r_in, 0.0), (STEM_OUT, 0.0), (STEM_OUT, gap - (flat - STEM_OUT) * slope), (flat, gap),
            (lip, gap), (lip, HOOK_H), (r_in + tip, HOOK_H), (r_in, HOOK_H - tip)]


def hook(start_deg, span_deg, kind):
    """A wedge hook from start_deg counter-clockwise through span_deg, standing on z = 0.

    Lofted through one cross-section per degree; the lip gap opens from LIP_GAP_TRAILING at the
    start to LIP_GAP_LEADING at the end, the end that goes under the cushion's ledge first.
    """
    lip = dim("LIP_OUTER_RADIUS")[kind]
    n = max(8, math.ceil(span_deg))
    wires = []
    for i in range(n + 1):
        gap = dim("LIP_GAP_TRAILING") + i / n * (dim("LIP_GAP_LEADING") - dim("LIP_GAP_TRAILING"))
        ang = start_deg + span_deg * i / n
        wires.append(Wire.make_polygon([polar(r, ang, z) for r, z in hook_profile(gap, kind)], close=True))
    solid = Solid.loft(wires, True)
    # 45-degree lead-in on both ends of the lip, seen from above, so it finds the slot.
    r0, r1 = STEM_OUT, lip + 1.0
    ramp = math.degrees(dim("LIP_END_RAMP") / lip)
    for end, sign in ((start_deg, 1), (start_deg + span_deg, -1)):
        tip = end + sign * ramp * (r1 - r0) / (lip - r0)
        outline = [polar(r0, end - sign * 2, -1), polar(r0, end, -1), polar(r1, tip, -1), polar(r1, end - sign * 2, -1)]
        solid -= extrude(Face(Wire.make_polygon(outline, close=True)), HOOK_H + 2, dir=(0, 0, 1))
    return solid


def hook_spans():
    """(start angle, span, kind) of each hook, placed where it sits when the cushion is locked."""
    out = []
    for centre, kind in dim("SLOT_ANGLES"):
        centre = -centre   # the plate faces the cushion, so the photo's pattern is mirrored
        r_mid = (dim("STEM_INNER_RADIUS")[kind] + STEM_OUT) / 2
        span = math.degrees(dim("HOOK_LENGTH") / r_mid)
        chord = dim("SLOT_LONG_CHORD") if kind == "long" else dim("SLOT_SHORT_CHORD")
        half = math.degrees(math.asin(chord / (2 * SLOT_PITCH_RADIUS)))
        lead = centre + half - math.degrees(dim("LOCK_END_GAP") / r_mid)   # the ledge closes this end
        out.append((lead - span + dim("CUSHION_CLOCKING_DEG"), span, kind))
    return out


def pin_hole(x, y):
    """Through-hole cutter for a pin, chamfered at both mouths."""
    r, c, depth = dim("PIN_SLIP_HOLE") / 2, dim("PIN_HOLE_CHAMFER"), dim("PLATE_THICKNESS") - dim("RELIEF_DEPTH")
    low = (Align.CENTER, Align.CENTER, Align.MIN)
    return (Pos(x, y, -1) * Cylinder(r, depth + 2, align=low)
            + Pos(x, y, -1) * Cone(r + c + 1, r, c + 1, align=low)
            + Pos(x, y, depth - c) * Cone(r, r + c + 1, c + 1, align=low))

