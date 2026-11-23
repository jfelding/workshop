"""Slim printed shell for the DewertOkin / OKIN CLASSIC 27760 remote. It reuses the original PCB, the
two linked three-button strips, the cable with its strain-relief boot, and the three case screws.

    uv run python cad/remote_shell.py

Writes remote_front.stl and remote_back.stl (both in print orientation, outer face on the bed),
remote_shell.step (assembled, with the estimated internals) and remote_shell.png.

Axes: X along the remote (0 = button end, +X = cable end), Y across it, Z through it
(0 = back face, +Z = keypad face).

Where the numbers come from:
  * OEM STEP (vendor-dewertokin/classic/CLASSIC_6_keys.STEP): the button layout (3 across at
    15.0 pitch, rows 23.5 apart), ~10 mm button holes, dome tops 3.25 above the inside of the
    keypad wall, the cable boot (~10 mm), the centre case screw through the PCB hole, Ø5.5 heads.
  * User: PCB 40 x 50.
  * User, caliper (2026-11-02): PCB 1.70 thick; PCB underside to the top of the switches 11.6;
    button strip 41.9 across (11.13 is probably its size across the buttons, not its height); centre hole
    Ø9, edges 19.7 from the cable end / 21.0 from the button end, centred across; head = left column (cable up).
  * Photos (estimates): switches ~6.8 x 20 at the PCB corners, solder-side clearance.
"""
import pathlib
from build123d import *
from workshop.cad.export import export

EXPORTS = pathlib.Path(__file__).parent.parent / "exports"

# --- hardware (MEASURE the starred ones; each is one caliper reading) ----------------------
PCB_W, PCB_L = 40.0, 50.0   # user
PCB_T = 1.70                # user
PCB_HOLE = 9.0              # user
HOLE_DX = +0.65             # hole centre from the PCB centre, + = towards the cable end (user:
                            #   edges 19.7 from the cable end, 21.0 from the button end)
UNDER_GAP = 2.8             # least room for solder joints + wires under the board (LIFT adds to it)
SWITCH_H = 11.6 - PCB_T     # user: PCB top face to the top of the switches
# The button strips sit partly beside the switches, so how far their bodies stand above the switch
# tops isn't measured. The front half is made for the most it can be; the back half's supports lift
# the board to suit the real parts (LIFT, set from a dry fit in the printed front half, see README).
STRIP_UP_MAX = 5.0          # the OEM case leaves room for at most ~4.5
STRIP_UP_EST = 3.6          # estimate: fills the OEM case's ~18.5 interior
DRYFIT_D = None             # * dry fit: how far the board's underside stands proud of the front half's
                            #   rim (mm; negative if below it). None = use the estimate.
DOME_D = 9.6                # strip dome diameter (OEM hole ~10.0)
DOME_ABOVE_CEIL = 3.25      # dome top above the inside of the keypad wall (OEM STEP)
PITCH_Y, ROW_DX = 15.0, 23.5  # button pitch across, row spacing along (OEM STEP)
BOOT_D = 9.8                # cable boot where it leaves the case (OEM ~9.6-10)
SCREW_CLR, SCREW_PILOT = 3.2, 2.4   # OEM case screws assumed ~2.9 mm self-tappers
HEAD_D, HEAD_H = 6.0, 2.4   # counterbore for the Ø5.5 pan heads

# --- shell design ---------------------------------------------------------------------------
WALL = 2.2
W = 50.0                    # at the keypad: keeps ~1 mm of flat face outside the outer holes
W_END = 40.0                # at the cable end: the plan tapers past the PCB, where only the clamp is
TAPER_X = 58.0              # where the taper starts (PCB ends at 54.2)
L = 86.0
R_BTN, R_CBL, R_WAIST = 6.0, 12.0, 40.0   # plan radii: button corners, cable corners, taper knee
BACK_CH, BACK_FIL = 3.0, 5.0     # back edge: 45 deg chamfer (prints on the bed) blended by a fillet
FRONT_CH, FRONT_FIL = 1.5, 2.5   # keypad edge: same, tighter
HOLE_D = DOME_D + 0.7
LIP_H, LIP_CLR = 1.5, 0.15
TUBE_R = PCB_HOLE / 2 - 0.25        # centre tube: a sliding fit in the PCB hole
# engraved column marks between the rows: head = circle, legs = line, middle (both) = the two as a
# figure, circle above line ("above" = towards the cable end, the top in the hand)
HEAD_Y = PITCH_Y            # user: head = left-hand column with the cable up and the keypad facing you
STRIP_W = 41.9              # user: button strip length across
MARK_DEPTH, MARK_W = 0.2, 0.8   # one layer deep (easy to wipe; fill with epoxy/polish), two lines wide

pcb_x0 = WALL + 2.0                 # room for the switches overhanging the button end
pcb_xc = pcb_x0 + PCB_L / 2
pcb_z0 = WALL + UNDER_GAP           # lowest board position (LIFT = 0); fixes the front half's geometry
pcb_z1 = pcb_z0 + PCB_T
ceil = pcb_z1 + SWITCH_H + STRIP_UP_MAX   # inside of the keypad wall
T = ceil + WALL                     # overall thickness
SEAM = pcb_z1 + 1.0                 # parting plane = cable centreline
# how far the back half's supports raise the board; 0.2 mm short so the strips are never pre-pressed
LIFT = (SEAM - DRYFIT_D - pcb_z0 - 0.2) if DRYFIT_D is not None else (STRIP_UP_MAX - STRIP_UP_EST - 0.2)
assert LIFT >= 0, "the parts stand taller than STRIP_UP_MAX allows: raise STRIP_UP_MAX and reprint the front"
board_z0 = pcb_z0 + LIFT
board_z1 = board_z0 + PCB_T
centre = (pcb_xc + HOLE_DX, 0.0)   # the PCB hole: the centre screw, and (as on the OEM) the rows' centre
row_xs = [centre[0] - ROW_DX / 2, centre[0] + ROW_DX / 2]
col_ys = [-PITCH_Y, 0.0, PITCH_Y]
clamp_x0 = L - 16.0                 # inner end of the cable clamp
case_screws = [(L - 15.0, -11.6), (L - 15.0, 11.6)]   # beside the clamp block (±7.5)


def plan(inset=0.0):
    """Outline: full width over the keypad, tapering to W_END at the cable end; inset by `inset`."""
    with BuildSketch() as s:
        Polygon((0, -W / 2), (TAPER_X, -W / 2), (L, -W_END / 2), (L, W_END / 2), (TAPER_X, W / 2), (0, W / 2),
                align=None)
        fillet(s.vertices().filter_by_position(Axis.X, TAPER_X - .1, TAPER_X + .1), radius=R_WAIST)
        fillet(s.vertices().filter_by_position(Axis.X, L - .1, L + .1), radius=R_CBL)
        fillet(s.vertices().filter_by_position(Axis.X, -.1, .1), radius=R_BTN)   # re-query each time
        if inset:
            offset(amount=-inset, mode=Mode.REPLACE)
    return s.sketch


def zcyl(x, y, r, z0, z1):
    return Cylinder(r, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, y, z0)))


def xcyl(r, x0, x1, z=SEAM):
    return Cylinder(r, x1 - x0, rotation=(0, 90, 0), align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
        Location((x0, 0, z)))


def slab(inset, z0, z1):
    return extrude(plan(inset).moved(Location((0, 0, z0))), amount=z1 - z0)


def body():
    b = slab(0, 0, T)
    b = chamfer(b.edges().group_by(Axis.Z)[0], length=BACK_CH)
    b = chamfer(b.edges().group_by(Axis.Z)[-1], length=FRONT_CH)
    b = fillet(b.edges().filter_by_position(Axis.Z, BACK_CH - .01, BACK_CH + .01), radius=BACK_FIL)
    b = fillet(b.edges().filter_by_position(Axis.Z, T - FRONT_CH - .01, T - FRONT_CH + .01), radius=FRONT_FIL)
    return b


def cavity():
    c = slab(WALL, WALL, ceil)
    c = fillet(c.edges().group_by(Axis.Z)[0], radius=BACK_CH + 1.0)
    c = fillet(c.edges().group_by(Axis.Z)[-1], radius=1.0)   # flat ceiling reaches the strips' end blocks
    return c


def cable_clamp():
    """Block round the boot, bored to BOOT_D with three ribs that bite 0.6 into it."""
    blk = Box(L - WALL - clamp_x0 + 1, 2 * 7.5, ceil - WALL, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(
        Location((clamp_x0, 0, WALL)))
    blk -= xcyl(BOOT_D / 2 - 0.6, clamp_x0 - 1, L + 1)
    for x0 in (clamp_x0 + 1.2, clamp_x0 + 5.6, clamp_x0 + 10.0):
        blk -= xcyl(BOOT_D / 2, x0, x0 + 3.2)
    return blk


def shells():
    outer, cav = body(), cavity()
    shell = outer - cav + cable_clamp()
    shell -= xcyl(BOOT_D / 2 + 0.2, L - WALL - 2, L + 1)      # exit through the end wall
    lower = Box(400, 400, SEAM + 100, align=(Align.CENTER, Align.CENTER, Align.MAX)).moved(Location((0, 0, SEAM)))
    back, front = shell & lower, shell - lower

    # seam: lip on the back half, matching rebate in the front half; flush outside (no groove to collect dirt)
    lip = slab(WALL / 2 + LIP_CLR, SEAM, SEAM + LIP_H) - slab(WALL, SEAM - 1, SEAM + LIP_H + 1)
    at_clamp = Box(L - clamp_x0 + 2, 15.4, 10, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(
        Location((clamp_x0 - 1, 0, SEAM - 1)))                 # no lip where the clamp block crosses the seam
    back += lip - at_clamp
    front -= slab(WALL / 2, SEAM - 1, SEAM + LIP_H + 0.2) - slab(WALL + 1, SEAM - 2, SEAM + 3) - at_clamp

    # --- back half: PCB supports (all at board_z0, i.e. raised by LIFT), screw bosses ---
    seat = zcyl(*centre, PCB_HOLE / 2 + 1.0, WALL - 0.5, board_z0)        # 1 mm rim round the hole
    back += seat - zcyl(*centre, TUBE_R + 0.2, pcb_z0, board_z0 + 1)      # the front's tube lands at pcb_z0
    back += Box(1.2, 16, board_z0 - WALL + 0.5, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(
        Location((pcb_x0, 0, WALL - 0.5)))                                  # button-end ledge (between switches)
    for sy in (-1, 1):
        back += Box(1.5, 3, board_z0 - WALL + 0.5, align=(Align.MAX, Align.CENTER, Align.MIN)).moved(
            Location((pcb_x0 + PCB_L, sy * 9, WALL - 0.5)))                 # cable-end pads, wires pass between
        g = PCB_W / 2 + 0.3                                                 # side guides, mid-board (clear of switches)
        back += Box(8, 1.3, board_z1 - WALL + 0.5,
                    align=(Align.CENTER, Align.MIN if sy > 0 else Align.MAX, Align.MIN)).moved(
            Location((pcb_xc, sy * g, WALL - 0.5)))
    for x, y in case_screws:
        back += zcyl(x, y, 3.6, WALL - 0.5, SEAM)
    for x, y in case_screws + [centre]:
        back -= zcyl(x, y, SCREW_CLR / 2, -1, SEAM + 5)
        back -= zcyl(x, y, HEAD_D / 2, -1, HEAD_H)

    # --- front half: button holes, centre clamp boss, screw bosses ---
    for x in row_xs:
        for y in col_ys:
            front -= zcyl(x, y, HOLE_D / 2, ceil - 1, T + 1)
            front -= Cone(HOLE_D / 2 + 0.6, HOLE_D / 2, 0.6, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
                Location((x, y, ceil)))                                       # lead-in for the dome
            front -= Cone(HOLE_D / 2, HOLE_D / 2 + 0.5, 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
                Location((x, y, T - 0.5)))                                    # softened rim
    front -= marks()
    front += zcyl(*centre, TUBE_R, pcb_z0, ceil + 0.5)    # tube through the PCB hole onto the back's seat:
                                                            # locates the board, takes the centre screw
    for x, y in case_screws:
        front += zcyl(x, y, 3.6, SEAM, ceil + 0.5)
    for x, y in case_screws + [centre]:
        front -= zcyl(x, y, SCREW_PILOT / 2, SEAM - 5, ceil - 0.3)
    return back, front


def marks():
    """Engraving cutters on the keypad face: circle (head), line (legs), circle over line (both)."""
    def ring(x, y):
        return zcyl(x, y, 2.0, T - MARK_DEPTH, T + 1) - zcyl(x, y, 2.0 - MARK_W, T - 2, T + 2)

    def line(x, y):
        return Box(5.0, MARK_W, MARK_DEPTH + 1, align=(Align.MAX, Align.CENTER, Align.MIN)).moved(
            Location((x, y, T - MARK_DEPTH)))
    x0 = centre[0]
    xc, xl = x0 + 2.7, x0 + 0.2        # circle centre, top end of the line
    return ring(xc, HEAD_Y) + ring(xc, 0) + line(xl, 0) + line(xl, -HEAD_Y)


def internals():
    """Estimated stand-in for the original parts: PCB, switches, strips, cable boot."""
    pcb = Box(PCB_L, PCB_W, PCB_T, align=(Align.MIN, Align.CENTER, Align.MIN)).moved(Location((pcb_x0, 0, board_z0)))
    pcb -= zcyl(*centre, PCB_HOLE / 2, board_z0 - 1, board_z1 + 1)
    sw_top = board_z1 + SWITCH_H                   # the strips rest on the switches
    top = sw_top + STRIP_UP_EST                    # strip bodies' top (estimate)
    switches = [Box(20, 6.8, SWITCH_H, align=(Align.MIN if sx < 0 else Align.MAX, Align.CENTER, Align.MIN)).moved(
        Location((pcb_x0 - 0.8 if sx < 0 else pcb_x0 + PCB_L + 0.8, sy * (PCB_W / 2 - 3.4), board_z1)))
        for sx in (-1, 1) for sy in (-1, 1)]
    strips = []
    for x in row_xs:
        bar = Box(10, STRIP_W, 2.6, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(Location((x, 0, sw_top)))
        ends = [Box(10, 4, top - sw_top - 2.6, align=(Align.CENTER, Align.CENTER, Align.MIN)).moved(
            Location((x, sy * (STRIP_W / 2 - 2), sw_top + 2.6))) for sy in (-1, 1)]
        domes = [zcyl(x, y, DOME_D / 2, sw_top + 2.6, top + DOME_ABOVE_CEIL) for y in col_ys]
        strips.append(Part() + [bar] + ends + domes)
    boot = xcyl(BOOT_D / 2 - 0.6, clamp_x0 - 2, L + 29) + xcyl(BOOT_D / 2, clamp_x0 + 1.2, clamp_x0 + 4.4)
    return {"pcb": pcb, "switches": Part() + switches, "strips": Part() + strips, "boot": boot}


def overlap(a, b):
    o = a & b
    return 0.0 if o is None else o.volume


def shade(parts, elev, azim, px=700):
    """Small z-buffer rasteriser (orthographic, two-sided Lambert): returns an RGB image."""
    import numpy as np, math
    e, a = math.radians(elev), math.radians(azim)
    d = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])   # towards the eye
    r = np.cross(-d, [0, 0, 1.0]); r /= np.linalg.norm(r); u = np.cross(r, -d)
    light = 0.6 * d + 0.5 * u + 0.3 * r; light /= np.linalg.norm(light)
    tris = []
    for shape, rgb in parts:
        vs, ts = shape.tessellate(0.05, 0.2)
        v = np.array([tuple(q) for q in vs]); t = v[np.array(ts)]
        n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]); n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        k = 0.25 + 0.75 * np.abs(n @ light)
        tris.append((np.stack([t @ r, t @ u, t @ d], axis=-1), np.outer(k, rgb)))
    allp = np.concatenate([t for t, _ in tris]).reshape(-1, 3)
    lo, hi = allp.min(0), allp.max(0)
    s = (px - 20) / max(hi[0] - lo[0], hi[1] - lo[1])
    H, Wd = int((hi[1] - lo[1]) * s) + 20, int((hi[0] - lo[0]) * s) + 20
    img = np.ones((H, Wd, 3)); zb = np.full((H, Wd), -np.inf)
    for t, col in tris:
        X = (t[..., 0] - lo[0]) * s + 10; Y = (hi[1] - t[..., 1]) * s + 10; Z = t[..., 2]
        for i in range(len(t)):
            x, y, z = X[i], Y[i], Z[i]
            x0, x1 = max(int(x.min()), 0), min(int(x.max()) + 1, Wd - 1)
            y0, y1 = max(int(y.min()), 0), min(int(y.max()) + 1, H - 1)
            if x1 < x0 or y1 < y0:
                continue
            gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + .5, np.arange(y0, y1 + 1) + .5)
            den = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
            if abs(den) < 1e-9:
                continue
            w0 = ((y[1] - y[2]) * (gx - x[2]) + (x[2] - x[1]) * (gy - y[2])) / den
            w1 = ((y[2] - y[0]) * (gx - x[2]) + (x[0] - x[2]) * (gy - y[2])) / den
            w2 = 1 - w0 - w1
            m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            zz = w0 * z[0] + w1 * z[1] + w2 * z[2]
            sub = zb[y0:y1 + 1, x0:x1 + 1]
            m &= zz > sub
            sub[m] = zz[m]
            img[y0:y1 + 1, x0:x1 + 1][m] = col[i]
    # outlines where the depth jumps (silhouettes, holes, the 0.4 mm engravings)
    z = np.where(np.isfinite(zb), zb, zb[np.isfinite(zb)].min() - 50)
    d2y = np.abs(z[2:, 1:-1] - 2 * z[1:-1, 1:-1] + z[:-2, 1:-1])   # second differences: a smooth slope
    d2x = np.abs(z[1:-1, 2:] - 2 * z[1:-1, 1:-1] + z[1:-1, :-2])   # gives ~0, a step stands out
    edge = np.zeros(z.shape, bool)
    edge[1:-1, 1:-1] = (d2y > 0.1) | (d2x > 0.1)
    img[edge] *= 0.35
    return np.clip(img, 0, 1)


def render(back, front, inn, path):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    dark, mid = (0.32, 0.33, 0.35), (0.40, 0.41, 0.43)
    kit = [(inn["pcb"], (0.2, 0.55, 0.3)), (inn["switches"], (0.12, 0.12, 0.12)),
           (inn["strips"], (0.18, 0.18, 0.2)), (inn["boot"], (0.12, 0.12, 0.12))]
    fig, axs = plt.subplots(2, 4, figsize=(22, 10.5))
    for ax, parts, el, az, t in [
            (axs[0, 0], [(back, dark), (front, mid), (inn["strips"], (0.18, 0.18, 0.2)), (inn["boot"], (0.12, 0.12, 0.12))], 40, -120, "keypad side"),
            (axs[0, 1], [(back, dark), (front, mid), (inn["boot"], (0.12, 0.12, 0.12))], -40, -120, "back: three case screws"),
            (axs[0, 2], [(back, dark)] + kit, 55, -120, "back half + original parts (estimated)"),
            (axs[1, 0], [(front, mid)], -55, -120, "front half, inside"),
            (axs[0, 3], [(front, mid), (inn["strips"], (0.18, 0.18, 0.2))], 89, -90,
             f"keypad (cable end right); in the hand, cable up: head = {'right' if HEAD_Y < 0 else 'left'} column")]:
        ax.imshow(shade(parts, el, az)); ax.set_axis_off(); ax.set_title(t, fontsize=10)
    for ax, (pl, ix, iy, t) in zip(axs[1, 1:3], [(Plane.XZ, "X", "Z", "section on the centreline (Y = 0)"),
                                                (Plane.YZ.offset(row_xs[0]), "Y", "Z", "section through a button row")]):
        for shape, col in [(back, "#555"), (front, "#999"), (inn["pcb"], "#3a8c4f"), (inn["switches"], "#222"),
                           (inn["strips"], "#333"), (inn["boot"], "#111")]:
            sec = shape & pl
            if sec is None:
                continue
            for f in sec.faces():
                for w in [f.outer_wire()] + f.inner_wires():
                    pts = [w.position_at(j / 200) for j in range(201)]
                    ax.fill([getattr(q, ix) for q in pts], [getattr(q, iy) for q in pts], color=col, ec="k", lw=.3)
        ax.set_aspect("equal"); ax.set_title(t, fontsize=10); ax.grid(lw=.2)
    axs[1, 3].set_axis_off()
    fig.suptitle(f"CLASSIC 27760 slim shell: {L:.0f} x {W:.0f} x {T:.1f} mm (OEM 139.5 x 50 x 23.5)")
    fig.savefig(path, dpi=95, bbox_inches="tight")


if __name__ == "__main__":
    out = EXPORTS
    back, front = shells()
    inn = internals()
    print(f"envelope {L:.1f} x {W:.1f} x {T:.1f} mm; seam at Z {SEAM:.1f}; board lifted {LIFT:.2f} "
          f"({'dry fit' if DRYFIT_D is not None else 'estimate'}), at {board_z0:.1f}-{board_z1:.1f}; buttons stand "
          f"{board_z1 + SWITCH_H + STRIP_UP_EST + DOME_ABOVE_CEIL - T:.2f} proud (estimate)")
    if DRYFIT_D is None:
        print(f"dry fit: expect the board's underside about {SEAM - board_z0 - 0.2:.1f} mm proud of the front half's rim")
    print(f"back {back.volume / 1000:.1f} cm^3, front {front.volume / 1000:.1f} cm^3, "
          f"back/front overlap {overlap(back, front):.2f} mm^3")
    for k, v in inn.items():
        print(f"  {k:9s} vs back {overlap(v, back):6.2f}  vs front {overlap(v, front):6.2f} mm^3 (want 0)")
    export("remote_back", back, out)
    export("remote_front", front.rotate(Axis.X, 180).moved(Location((0, 0, T))), out)
    asm = Compound(children=[back, front] + list(inn.values()))
    export_step(asm, str(out / "remote_shell.step"))
    render(back, front, inn, out / "remote_shell.png")
