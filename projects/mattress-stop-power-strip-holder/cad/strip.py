"""Elworks 6-stikdåse u/jord (39-306-1), as measured by the user on 2026-11-02.

    strip(length, width, height)   the body, sockets on top, plus holes in the base, cable stub

Local axes: X along the strip (cable end at +X), Y across, Z up from the base; base centred.
Measured (calipers, along the centreline unless noted):
  * body 284 long (without the cord's strain relief), 44.5 wide, 35.85 base to socket face;
  * 6 socket recesses, 38 diameter, 14 deep; the first starts 19.7 from the cord end, the last
    ends 4.95 from the far end (so centres 38.7 and 23.95 from the ends, pitch 44.27);
  * the plan's corners are rounded: CORNER_R = 12.5 reproduces both corner-to-socket distances
    the user took (20.3 at the cord end, 8.9 at the far end; see corner_report()). The long
    faces narrow a little over the last ~22 mm, which that radius stands in for;
  * two plus-shaped hanging holes in the base, on the centreline: their arm tips are 55.9 from
    the cord end and 42.0 from the far end, 17.5 from the long faces. Behind the 2 mm base wall
    each has a square pocket a little wider than the plus, 3.65 deep. Plus: 9.5 across, round arm
    ends about 3 in diameter, 6.25-6.5 between opposite inner corners (a round middle).
Not measured: where the cable leaves the end (CABLE_Z, from the old sketch); the arm neck width
(PLUS_ARM_W, from the photo).
"""
from build123d import *

LENGTH, WIDTH, HEIGHT = 284.0, 44.5, 35.85
CORNER_R = 12.5
TOP_FILLET = 2.0
N_SOCKETS, SOCKET_D, RECESS = 6, 38.0, 14.0
SOCKET_CORD_GAP, SOCKET_FAR_GAP = 19.7, 4.95      # end face to socket edge, on the centreline
# plus-shaped hanging holes in the base
PLUS_SPAN, PLUS_LOBE_D, PLUS_MID_D = 9.5, 3.0, 6.4   # across, arm-end diameter, round middle
PLUS_ARM_W = 2.8                                     # neck of each arm (photo: a bit under the lobe)
PLUS_TIP_CORD, PLUS_TIP_FAR = 55.9, 42.0             # end face to the nearest arm tip
BASE_WALL, POCKET_D, POCKET_W = 2.0, 3.65, 10.0      # POCKET_W: "a tiny bit more than the plus"
CABLE_Z, CABLE_D, RELIEF_D, RELIEF_L, CABLE_STUB = 10.0, 6.2, 10.0, 9.0, 22.0


def socket_xs(length=LENGTH):
    """Socket centres along X (from the strip's middle), evenly spaced between the measured end gaps."""
    a = length / 2 - SOCKET_CORD_GAP - SOCKET_D / 2          # cord end is +X
    b = -length / 2 + SOCKET_FAR_GAP + SOCKET_D / 2
    return [b + i * (a - b) / (N_SOCKETS - 1) for i in range(N_SOCKETS)]


def plus_xs(length=LENGTH):
    """Centres of the two plus holes along X (far end, cord end)."""
    return [-length / 2 + PLUS_TIP_FAR + PLUS_SPAN / 2, length / 2 - PLUS_TIP_CORD - PLUS_SPAN / 2]


def plus_sketch(span=PLUS_SPAN, arm_w=PLUS_ARM_W, lobe_d=PLUS_LOBE_D, mid_d=PLUS_MID_D):
    """The plus outline in a local XY plane, arms along X and Y."""
    reach = span / 2 - lobe_d / 2
    with BuildSketch() as sk:
        Circle(mid_d / 2)
        for a in (0, 90):
            Rectangle(2 * reach, arm_w, rotation=a)
        with PolarLocations(reach, 4):
            Circle(lobe_d / 2)
    return sk.sketch


def plus_cavity():
    """Opening through the base wall plus the square pocket behind it, at the origin, Z up
    from the outside of the base (Z = 0)."""
    opening = extrude(plus_sketch(), amount=BASE_WALL)
    pocket = Box(POCKET_W, POCKET_W, POCKET_D, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((0, 0, BASE_WALL)))
    return opening + pocket


def strip(length=LENGTH, width=WIDTH, height=HEIGHT):
    with BuildPart() as p:
        with BuildSketch():
            RectangleRounded(length, width, CORNER_R)
        extrude(amount=height)
        fillet(p.edges().group_by(Axis.Z)[-1], radius=TOP_FILLET)
        with Locations(*[(x, 0, height) for x in socket_xs(length)]):
            Cylinder(min(SOCKET_D, width - 3) / 2, RECESS, align=(Align.CENTER, Align.CENTER, Align.MAX),
                     mode=Mode.SUBTRACT)
        for x in plus_xs(length):
            insert(plus_cavity().moved(Location((x, 0, 0))), mode=Mode.SUBTRACT)
        # strain relief and a stub of cable at the +X end
        with Locations(Location((length / 2 - 1, 0, CABLE_Z), (0, 90, 0))):
            Cylinder(RELIEF_D / 2, RELIEF_L, align=(Align.CENTER, Align.CENTER, Align.MIN))
        with Locations(Location((length / 2 + RELIEF_L - 2, 0, CABLE_Z), (0, 90, 0))):
            Cylinder(CABLE_D / 2, CABLE_STUB, align=(Align.CENTER, Align.CENTER, Align.MIN))
    return p.part


def corner_report():
    """Socket edge to the middle of each rounded corner (cord end, far end), against 20.3 / 8.9."""
    import math
    xs = socket_xs()
    out = []
    for xc, end in ((xs[-1], LENGTH / 2), (xs[0], -LENGTH / 2)):
        cx = math.copysign(abs(end) - CORNER_R, end)
        k = CORNER_R / math.sqrt(2)
        out.append(math.hypot(cx + math.copysign(k, end) - xc, WIDTH / 2 - CORNER_R + k) - SOCKET_D / 2)
    return out


if __name__ == "__main__":
    s = strip()
    bb = s.bounding_box()
    xs = socket_xs()
    print(f"strip {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.2f} mm (incl. cable stub), "
          f"socket pitch {xs[1] - xs[0]:.2f}, plus centres {[round(x, 2) for x in plus_xs()]}")
    c, f = corner_report()
    print(f"corner R {CORNER_R}: socket edge to corner {c:.1f} at the cord end (measured 20.3), "
          f"{f:.1f} at the far end (measured 8.9)")
    export_step(s, "strip_6socket.step")
