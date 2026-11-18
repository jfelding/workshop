"""Dyson half of the adapter: an oval plate with four wedge hooks for the cushion's twist lock.

    uv run python cad/dyson_half.py        # writes exports/dyson_half.{stl,step,png}

The outline is the Bose frame's oval, so the two halves glue back to back with flush edges. The
plate is 1.2 mm thick with a 0.8 mm raised seat inside the hooks; only the seat touches the
cushion, and the cushion's proud ledge blocks pass over the lower part. Each hook is a stem with
an outward lip whose gap to the seat narrows along its length (a wedge), so twisting the cushion
draws it down onto the seat and clamps it.

The plate and the hook pattern are both 180-degree symmetric and the left and right cushions are
identical, so one part serves both ears.
"""
import math
from pathlib import Path

from build123d import (Align, Axis, Circle, Cone, Cylinder, Ellipse, Face, GeomType, Pos, Solid, Wire,
                       chamfer, extrude, fillet)

from workshop.cad.checks import fits_bed
from workshop.cad.export import export
from workshop.measure import dims

import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
BED = (220, 220, 270)   # Neptune 3 Pro, from equipment/neptune-3-pro
NAME = "dyson_half"

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
    solid = Solid.make_loft(wires, True)
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


def make():
    t = dim("PLATE_THICKNESS")
    low = t - dim("RELIEF_DEPTH")
    bore = Circle(dim("BORE_DIAMETER") / 2)
    plate = extrude(Ellipse(dim("BOSE_OVAL_X") / 2, dim("BOSE_OVAL_Y") / 2) - bore, low)
    rim = plate.edges().filter_by(GeomType.ELLIPSE).sort_by(Axis.Z)
    plate = chamfer(rim[0], dim("BACK_EDGE_CHAMFER"))
    plate = fillet(plate.edges().filter_by(GeomType.ELLIPSE).sort_by(Axis.Z)[-1], dim("FRONT_EDGE_FILLET"))
    seat = extrude(Circle(STEM_OUT) - bore, t)   # the only face that touches the cushion
    seat = fillet(seat.edges().filter_by(GeomType.CIRCLE).group_by(Axis.Z)[-1].sort_by(lambda e: e.radius)[0],
                  dim("BORE_EDGE_FILLET"))
    part = plate + seat
    for x, y in pin_positions():
        part -= pin_hole(x, y)
    for start, span, kind in hook_spans():
        part += Pos(0, 0, t) * hook(start, span, kind)
    return part


if __name__ == "__main__":
    part = make()
    assert fits_bed(part, BED)
    size = part.bounding_box().size
    print(f"pins at {[(round(x, 2), round(y, 2)) for x, y in pin_positions()]}, "
          f"hooks at {[(round(s, 1), round(sp, 1), k) for s, sp, k in hook_spans()]}")
    assert abs(size.X - dim("BOSE_OVAL_X")) < 0.01 and abs(size.Y - dim("BOSE_OVAL_Y")) < 0.01
    export(NAME, part, OUT, tolerance=0.01, angular_tolerance=0.1)
