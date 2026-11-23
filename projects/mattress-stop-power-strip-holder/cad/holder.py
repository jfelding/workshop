"""Shared base of the mattress-stop holder: the stop's dimensions, the module frame, the joint
blocks and bowtie keys every module end uses, extension lengths, and the remote cup.
The power-strip modules themselves are in holder_side.py, the magnet mount in holder_mag.py.

    uv run python cad/holder.py

Writes cup.stl, key.stl and panel_keepout.stl.

Axes (as used on the bed): X along the stop's top bar, Y towards the room (+Y), Z up.
The stop's top bar, in its tight fabric sleeve, touches Y = 0 (room side) and Z = 0 (top).
"""
import pathlib
from build123d import *
from workshop.cad.export import export

EXPORTS = pathlib.Path(__file__).parent.parent / "exports"

# --- the stop (MEASURE the starred one) -------------------------------------------------
PANEL_W = 126.0   # outer length of the top bar (user: "just over 126")
PANEL_H = 58.0    # visible height of the upright (user)
SLEEVE_D = 12.0   # 8 mm rod in a sleeve that sits tight (user): ~2 mm of fabric each side
# --- the remote (original CLASSIC case; a slim printed shell would get its own holder) -----------
REMOTE_W = 50.0   # remote width (DewertOkin CLASSIC 6-key STEP; caliper-check)
REMOTE_T = 23.5   # remote thickness, keypad face to back (STEP)
REMOTE_END_R = 25.0  # cable end is a full semicircle (STEP)
# --- design ---------------------------------------------------------------------------
WALL = 2.8
CLR = 0.8          # slack around the panel
CUP_DEPTH = 72.0
CUP_CLR = 3.0      # slack around the remote
SLOT_W = 9.0       # cable slit in the cup's back wall
# joint: a bowtie key (narrow at the seam, wide inside) drops into blocks behind the back plate
JB_T, JB_L = 12.8, 10.0        # joint block thickness (Y) and length (X) at each module end
KEY_N, KEY_W, KEY_D = 4.0, 7.5, 8.0   # key: neck width, end width, depth into each module
KEY_CLR = 0.15

SADDLE_L = PANEL_W + 2 * (JB_L + 1)  # joint blocks sit clear of the panel's ends
tray_bot = -(PANEL_H - 6)            # stays above the step of the stop
y_back = CLR / 2                     # back of the back plate (outer face of panel + slack)
y_plate = y_back + WALL              # front of the back plate
z_top = CLR / 2 + WALL               # top of every module's back plate
jb_y0 = y_back - JB_T                # joint block spans Y [jb_y0, y_plate], behind the plate
jb_yc = (jb_y0 + y_back) / 2         # pocket centred behind the plate, clear of it


def stop_keepout(d=SLEEVE_D):
    """The stop as the hook sees it: sleeved top bar, the two sleeved legs, and the fabric web
    between them (assumed 2 mm, centred on the rods)."""
    r = d / 2
    bar = Cylinder(r, PANEL_W, rotation=(0, 90, 0)).moved(Location((0, -r, -r)))
    legs = [Cylinder(r, PANEL_H - r, align=(Align.CENTER, Align.CENTER, Align.MAX)).moved(
        Location((sx * (PANEL_W / 2 - r), -r, -r))) for sx in (-1, 1)]
    web = Box(PANEL_W - d, 2, PANEL_H - r, align=(Align.CENTER, Align.CENTER, Align.MAX)).moved(Location((0, -r, -r)))
    return bar + legs[0] + legs[1] + web


KEY_TOP = tray_bot + WALL + (z_top - tray_bot - WALL - 1)   # a key resting on a pocket floor ends here


def joint_block(x_end, inward, hang=False):
    """Block behind the back plate at a module end, with a half-bowtie pocket open to the seam.
    inward = +1 if the module lies on the +X side of the seam, -1 if on the -X side.
    hang=False: pocket open at the top with a floor; the key drops in and rests on it.
    hang=True: pocket open at the bottom with a roof at the key's top; the part slides up onto a
    key already resting in its neighbour and hangs from it (the cups)."""
    xa, xb = sorted((x_end, x_end + inward * JB_L))
    top = KEY_TOP + WALL if hang else z_top
    blk = Box(xb - xa, JB_T + WALL, top - tray_bot, align=(Align.MIN, Align.MIN, Align.MIN)).moved(
        Location((xa, jb_y0, tray_bot)))
    n, w = KEY_N / 2 + KEY_CLR, KEY_W / 2 + KEY_CLR
    d = KEY_D + KEY_CLR
    pts = [(x_end, jb_yc - n), (x_end + inward * d, jb_yc - w),
           (x_end + inward * d, jb_yc + w), (x_end, jb_yc + n)]
    z0, z1 = (tray_bot - 1, KEY_TOP) if hang else (tray_bot + WALL, z_top + 1)
    with BuildSketch(Plane.XY.offset(z0)) as sk:
        Polygon(*pts, align=None)
    pocket = extrude(sk.sketch, amount=z1 - z0)
    return blk - pocket


def cup(x_seam):
    """Remote cup whose +X side meets a seam at x_seam (mirror it for the other end)."""
    cw, ct = REMOTE_W + CUP_CLR, REMOTE_T + CUP_CLR
    end_r = min(REMOTE_END_R + CUP_CLR / 2, cw / 2 - 0.01)
    cx, cy = x_seam - cw / 2 - WALL, y_plate + ct / 2
    with BuildPart() as c:
        with Locations((cx, cy, tray_bot)):
            Box(cw + 2 * WALL, ct + 2 * WALL, CUP_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MIN))
        fillet(c.edges().filter_by(Axis.Z), radius=6)
        with BuildSketch(Plane.XZ) as pocket:  # local (x, y) = world (X, Z)
            with Locations((cx, tray_bot + WALL)):
                Rectangle(cw, CUP_DEPTH, align=(Align.CENTER, Align.MIN))
            fillet(pocket.vertices().group_by(Axis.Y)[0], radius=end_r)
        pocket_solid = extrude(pocket.sketch, amount=ct / 2, both=True, mode=Mode.PRIVATE)
        add(pocket_solid.moved(Location((0, cy, 0))), mode=Mode.SUBTRACT)
        # floor hole at the lowest point, plus a slit down the back wall and across the floor,
        # so the cable drops in from above and the plug never has to pass through
        with Locations((cx, cy, tray_bot)):
            Cylinder(6, WALL * 3, mode=Mode.SUBTRACT)
        with Locations((cx, cy, tray_bot - 1)):
            Box(SLOT_W, ct / 2 + WALL * 2, CUP_DEPTH + 2, mode=Mode.SUBTRACT,
                align=(Align.CENTER, Align.MAX, Align.MIN))
    # the cup's flat end must reach the seam for the joint block to attach
    stub = Box(WALL + 6, WALL, z_top - tray_bot, align=(Align.MAX, Align.MIN, Align.MIN)).moved(
        Location((x_seam, y_back, tray_bot)))
    return c.part + stub + joint_block(x_seam, -1, hang=True)


def key():
    # same taper as the pocket, stopped 0.2 mm short of its end
    n, d = KEY_N / 2, KEY_D - 0.2
    w = n + (KEY_W / 2 - n) * d / KEY_D
    pts = [(0, -n), (d, -w), (d, w), (0, n), (-d, w), (-d, -w)]
    with BuildSketch() as sk:
        Polygon(*pts, align=None)
    return extrude(sk.sketch, amount=z_top - tray_bot - WALL - 1)


if __name__ == "__main__":
    h = SADDLE_L / 2
    c = cup(-h)
    print(f"cup vs stop (11 mm sleeve): overlap {(c & stop_keepout(11.0)).volume:.2f} mm^3 (want 0)")
    out = EXPORTS
    for name, p in {"cup": c, "key": key()}.items():
        bb = p.bounding_box()
        print(f"{name:10s} {bb.size.X:6.1f} x {bb.size.Y:5.1f} x {bb.size.Z:5.1f} mm  {p.volume/1000:5.1f} cm^3")
        export(name, p, out)
    scratch = out.parent / "scratch"   # a check model, not a part: kept out of exports/
    scratch.mkdir(exist_ok=True)
    export_stl(stop_keepout(), str(scratch / "panel_keepout.stl"))
