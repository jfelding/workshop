"""Strip-specific adapter for the Elworks 6-way (strip.py): a bayonet head that locks into one of
the plus-shaped hanging holes in the strip's base, on a T-foot that drops into a T-slot on the
holder (rail.py profile). Print two.

    uv run python cad/adapter.py

Fitting: hold the adapter with its foot at 45 degrees to the strip, push the head through the
plus hole, turn it 45 degrees so the foot lies ACROSS the strip. The head's arms then sit behind the
plastic between the plus's arms, inside the square pocket (the plus is four-fold, so either 45-degree
turn locks). Do both, then lower the strip so the feet drop into the holder's vertical T-slots
(holder_side.py). In a slot the foot cannot turn, so the bayonet cannot undo itself.

Frame: the strip's local frame (strip.py), centred on the plus hole: Z = 0 is the outside of the
strip's base, +Z into the strip, X along the strip, Y across it. The foot hangs below Z = 0.
Prints foot down (Z up), no supports: the head's arms overhang the neck by under 2 mm.
"""
import math
import pathlib
from build123d import *
from workshop.cad.export import export

EXPORTS = pathlib.Path(__file__).parent.parent / "exports"
import rail as R
import strip as S

HEAD_SPAN = 9.0      # tip to tip; the plus is 9.5
HEAD_ARM_W = 2.4     # the plus's arm neck is about 2.8 (photo): 0.4 clearance
HEAD_MID_D = 5.6     # the plus's round middle is 6.25-6.5 across
NECK_D = 5.6         # round neck through the 2 mm base wall
NECK_L = S.BASE_WALL + 0.1
HEAD_T = S.POCKET_D - 0.35
OFFSETS = (0.0, 2.0, 2.5, 3.0)   # offset adapters exported (foot x-offset from the head, mm)


def head_sketch(angle=45.0):
    """Head outline; angle = 45 is the locked position, 0 the position that passes the plus."""
    with BuildSketch() as sk:
        Circle(HEAD_MID_D / 2)
        for a in (0, 90):
            SlotCenterToCenter(HEAD_SPAN - HEAD_ARM_W, HEAD_ARM_W, rotation=a)
    return sk.sketch.rotate(Axis.Z, angle)


def bayonet(angle=45.0):
    neck = Cylinder(NECK_D / 2, NECK_L, align=(Align.CENTER, Align.CENTER, Align.MIN))
    head = extrude(head_sketch(angle), amount=HEAD_T).moved(Location((0, 0, NECK_L)))
    return neck + head


def adapter(turn=0.0):
    """The whole adapter; turn rotates it about its axis (0 = locked, -45 = inserting)."""
    return (R.foot() + bayonet()).rotate(Axis.Z, turn)


PLATE_T = 2.0        # offset adapter: plate between the strip's base and the slot's front face


def offset_adapter(dx, t=PLATE_T):
    """Bayonet head at the origin, foot ACROSS the strip (along Y) at x = dx, joined by a plate t thick
    lying flat on the strip's base. For a strip whose hole spacing doesn't match the slot spacing:
    the strip then stands t further from the back plate. Turning it 180 deg moves the foot to -dx.
    Prints foot down like the plain adapter. The plate reaches only 1 mm past the bayonet's neck and
    the foot's neck, so its one-sided overhang beyond the foot's neck stays near dx + 1 mm."""
    foot = R.foot().rotate(Axis.Z, 90).moved(Location((dx, 0, -t)))
    neck_half = (R.SLOT_W - R.NECK_CLR_W) / 2
    x0 = min(-NECK_D / 2 - 1.0, dx - neck_half)
    x1 = max(NECK_D / 2 + 1.0, dx + neck_half)
    plate = Box(x1 - x0, R.FOOT_L, t, align=(Align.MIN, Align.CENTER, Align.MAX)).moved(Location((x0, 0, 0)))
    return foot + plate + bayonet()


def bearing_area():
    """Area of the locked head that sits behind solid base wall (inside the pocket, outside the plus)."""
    pocket = Rectangle(S.POCKET_W, S.POCKET_W)
    behind = (head_sketch(45) & pocket) - S.plus_sketch()
    return behind.area


def checks(verbose=True):
    """Fit of one adapter in a block of the strip's base around a plus hole."""
    base = Box(30, 30, 8, align=(Align.CENTER, Align.CENTER, Align.MIN)) - S.plus_cavity()
    out = {}
    # inserting: the head, at 0 degrees, swept straight through the base wall
    sweep = extrude(head_sketch(0), amount=S.BASE_WALL + HEAD_T + 2).moved(Location((0, 0, -HEAD_T - 1)))
    out["head passes the plus (0 deg)"] = (sweep & base).volume
    # turning: 1 degree steps from 0 to 45 with the head in the pocket
    worst = max((bayonet(a) & base).volume for a in range(0, 46))
    out["head turns in pocket, worst of 0..45 deg"] = worst
    out["locked adapter vs strip"] = (adapter() & base).volume
    pulled = adapter().moved(Location((0, 0, -0.3)))           # pull 0.3 mm off the strip
    out["pulled 0.3 mm: head bears on wall (want > 0)"] = (pulled & base).volume
    if verbose:
        for k, v in out.items():
            print(f"  {k:46s} {v:7.2f} mm^3")
        print(f"  bearing area behind the wall: {bearing_area():.1f} mm^2 "
              f"(4 arms; head {HEAD_T:.2f} thick in a {S.POCKET_D} deep pocket)")
    return out


if __name__ == "__main__":
    out = EXPORTS
    # the arm neck of the plus is from the photo: also export test heads 0.2 narrower and wider
    for w in (HEAD_ARM_W, HEAD_ARM_W - 0.2, HEAD_ARM_W + 0.2):
        HEAD_ARM_W = w
        print(f"head arms {w:.1f} wide:")
        checks()
        a = adapter()
        name = "adapter_elworks" if abs(w - 2.4) < 1e-9 else f"adapter_elworks_test_arm{w:.1f}"
        export(name, a, out)
    bb = a.bounding_box()
    print(f"adapter {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm, {a.volume / 1000:.2f} cm^3")
    # offset adapters (2026-11-06): the printed slots sit closer together than the strip's holes
    HEAD_ARM_W = 2.4
    base = Box(40, 30, 8, align=(Align.CENTER, Align.CENTER, Align.MIN)) - S.plus_cavity()
    for dx in OFFSETS:
        o = offset_adapter(dx)
        print(f"offset adapter {dx:.1f}: vs strip {(o & base).volume:.2f} mm^3 (want 0), "
              f"pulled 0.3 mm bears {(o.moved(Location((0, 0, -0.3))) & base).volume:.2f} (want > 0), {o.volume / 1000:.2f} cm^3")
        export(f"adapter_offset_{dx:.1f}", o, out)
