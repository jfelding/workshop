"""Magnet mount used by the strip holder (holder_side.py): a printed insert slid inside the cloth
cover stiffens it, and magnet pairs (insert <-> holder back plate, cloth between) hold the holder
flat against it. A short lip resting on the sleeved bar carries the weight.

    uv run python cad/holder_mag.py

Writes mag_insert.stl. holder_side.py imports holder_magnets(), top_lip() and insert().

Magnets: pockets in the insert open on its mattress side (prints flat, room face down, pockets
open upwards); pockets in the holder sit in bosses on the back plate's front face, open towards
the room. Press or glue them in, and check each pair attracts first.
"""
import pathlib
from build123d import *
from workshop.cad.export import export

EXPORTS = pathlib.Path(__file__).parent.parent / "exports"
import holder as H

# --- magnets (the user's 10 x 5 mm discs) ---------------------------------------------------
MAG_D, MAG_T = 10.0, 5.0      # disc diameter, thickness (user has 10 x 5 mm, 2026-11-05)
MAG_CLR = 0.15                # press fit, on the radius
SKIN = 0.6                    # plastic between magnet face and cloth
# One row, matching the insert printed 2026-11-05 (pockets at x = -42, -14, 14, 42). The holder
# leaves out x = -14: the near adapter's T-slot sits there, and a 5 mm magnet behind it would
# break into the slot's undercut.
MAG_X = (-42.0, -14.0, 14.0, 42.0)
HOLDER_MAG_X = (-42.0, 14.0, 42.0)
MAG_Z = (-41.5,)                # pocket top 0.7 below the rail, so the magnets press straight in
# --- the insert -------------------------------------------------------------------------
ROD_D = 8.0
INS_T = MAG_T + SKIN + 0.6    # magnet pocket + skin + floor under the pocket's open side
INS_TOP = -(H.SLEEVE_D + 2.5) # just below the bar
INS_BOT = -50.0               # * how far down the pocket goes (MEASURE: cover pulled half off)
INS_CORNER = 8.0              # chamfer at the top corners: the bar bends into the legs
# --- the top lip and the backup ties -------------------------------------------------------
LIP_GAP = 2.2                 # between the sleeved bar and the lip
LIP_DROP_M = 6.0              # the lip only locates now; the magnets do the holding

r = H.SLEEVE_D / 2
leg_x = H.PANEL_W / 2 - r
ins_yc = -r                    # insert centred on the plane of the rods
ins_room = ins_yc + INS_T / 2  # its room-side face
lip_yi = -H.SLEEVE_D - LIP_GAP  # inner face of the lip


def top_lip(x0, x1):
    """Roof over the sleeved bar plus a short mattress-side lip."""
    yo = lip_yi - H.WALL
    zr, zt = H.CLR / 2, H.z_top
    with BuildSketch(Plane.YZ) as sk:
        with Locations((yo, zr)):
            Rectangle(H.y_plate - yo, H.WALL, align=(Align.MIN, Align.MIN))
        with Locations((yo, zr - LIP_DROP_M)):
            Rectangle(H.WALL, LIP_DROP_M, align=(Align.MIN, Align.MIN))
    roof = extrude(sk.sketch, amount=x1 - x0 - 2 * H.JB_L).moved(Location((x0 + H.JB_L, 0, 0)))
    return roof


def _teardrop(r, y0, length, x, z, peak):
    """Disc along +Y from y0 with a 45 deg peak towards Z = peak (+1 or -1). The holder prints upside
    down, so a pocket's roof points -Z and a boss's underside +Z."""
    disc = Cylinder(r, length, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y0, z), (-90, 0, 0)))
    tip = Box(r, length, r, align=(Align.CENTER, Align.MIN, Align.CENTER)).moved(
        Location((x, y0, z + peak * r / 2 ** 0.5), (0, 45, 0)))
    return disc + tip


def holder_magnets():
    """Bosses on the front of the back plate that deepen it where the magnets sit, and the pockets
    (open towards the room, so the magnets press in after printing)."""
    depth = SKIN + MAG_T + 0.2
    boss_t = depth - H.WALL
    bosses, pockets = [], []
    for x in HOLDER_MAG_X:
        for z in MAG_Z:
            bosses.append(_teardrop(MAG_D / 2 + 2, H.y_plate, boss_t, x, z, +1))
            pockets.append(_teardrop(MAG_D / 2 + MAG_CLR, H.y_back + SKIN, MAG_T + 0.2, x, z, -1))
    return bosses, pockets


def insert():
    """Plate that slides up inside the cover between the legs, magnets towards the room."""
    hw = leg_x - ROD_D / 2 - 0.5
    c = INS_CORNER
    pts = [(-hw, INS_BOT), (hw, INS_BOT), (hw, INS_TOP - c), (hw - c, INS_TOP),
           (-hw + c, INS_TOP), (-hw, INS_TOP - c)]
    with BuildSketch(Plane.XZ) as sk:      # local (x, y) = world (X, Z), normal -Y
        Polygon(*pts, align=None)
    plate = extrude(sk.sketch, amount=INS_T).moved(Location((0, ins_room, 0)))
    for x in MAG_X:
        for z in MAG_Z:
            plate -= Cylinder(MAG_D / 2 + MAG_CLR, INS_T, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
                Location((x, ins_room - SKIN, z), (90, 0, 0)))     # opens towards the mattress
    return plate


def rods():
    """Bare 8 mm rods: the insert lives inside the cover, so only the steel must clear."""
    rr = ROD_D / 2
    bar = Cylinder(rr, H.PANEL_W, rotation=(0, 90, 0)).moved(Location((0, -r, -r)))
    legs = [Cylinder(rr, H.PANEL_H - r, align=(Align.CENTER, Align.CENTER, Align.MAX)).moved(
        Location((sx * leg_x, -r, -r))) for sx in (-1, 1)]
    return bar + legs[0] + legs[1]


if __name__ == "__main__":
    ins = insert()
    gap = H.y_back + SKIN - ins_room + SKIN
    print(f"insert/rods overlap {(ins & rods()).volume:.2f} mm^3 (want 0)")
    print(f"magnet face to magnet face: {gap:.1f} mm (two {SKIN} mm skins + cloth)")
    bb = ins.bounding_box()
    print(f"mag_insert {bb.size.X:6.1f} x {bb.size.Y:5.1f} x {bb.size.Z:5.1f} mm  {ins.volume/1000:5.1f} cm^3")
    export("mag_insert", ins, EXPORTS)
