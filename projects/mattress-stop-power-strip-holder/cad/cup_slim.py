"""Remote cup for the slim shell (remote_shell.py), in place of cup.stl. It keys onto the saddle's
cup end like the original cup, and its pocket follows the shell's tapered outline, so the remote
drops in cable end down and centres itself. The rim stays below the buttons, so they still work
while the remote is docked.

    uv run python cad/cup_slim.py

Writes cup_slim.stl and remote_slim_fit.png, and checks the fit.
"""
import pathlib
from build123d import *
from workshop.cad.export import export

EXPORTS = pathlib.Path(__file__).parent.parent / "exports"
import holder as H
import remote_shell as RS

CLR = 1.5                    # slack round the shell, each side
DEPTH = 38.0                 # pocket depth from the floor: rim at 48 mm from the button end, below
                             # the lower button row (its holes end at ~46)
T_TOT = RS.T + RS.DOME_ABOVE_CEIL - RS.WALL   # thickness over the domes
SLOT_W = 9.0                 # cable slit, as on the original cup
x_seam = -H.SADDLE_L / 2


def to_world(shape):
    """Shell frame (X along the remote, Z through it) -> holder frame: cable end down on the cup
    floor, back of the remote against the cup's back wall, keypad to the room, flush with the seam."""
    s = shape.rotate(Axis.Y, -90).rotate(Axis.Z, -90).rotate(Axis.Y, 180)   # X->-Z, Y->-X, Z->Y
    half = RS.W / 2 + CLR + H.WALL
    return s.moved(Location((x_seam - half, H.y_plate + CLR, H.tray_bot + H.WALL + RS.L)))


def cup_slim():
    x0 = RS.L - DEPTH
    outer = extrude(RS.plan(-CLR - H.WALL).moved(Location((0, 0, -CLR - H.WALL))), amount=T_TOT + 2 * (CLR + H.WALL))
    outer &= Box(DEPTH + H.WALL, 200, 200, align=(Align.MIN, Align.CENTER, Align.CENTER)).moved(Location((x0, 0, 0)))
    rims = [e for g in (outer.edges().group_by(Axis.Z)[0], outer.edges().group_by(Axis.Z)[-1]) for e in g
            if e.bounding_box().min.X > x0 + 0.1]                       # outline edges of the two big faces
    outer = fillet(rims, radius=2.5)
    pocket = extrude(RS.plan(-CLR).moved(Location((0, 0, -CLR))), amount=T_TOT + 2 * CLR)
    pocket &= Box(DEPTH + 1, 200, 200, align=(Align.MIN, Align.CENTER, Align.CENTER)).moved(Location((x0 - 1, 0, 0)))
    c = outer - pocket
    c -= RS.xcyl(6.0, RS.L - 1, RS.L + H.WALL + 1)                     # the boot leaves through the floor
    c -= Box(DEPTH + H.WALL + 2, SLOT_W, RS.SEAM + CLR + H.WALL + 1,   # slit: floor and back wall, so the
             align=(Align.MIN, Align.CENTER, Align.MAX)).moved(Location((x0 - 1, 0, RS.SEAM)))  # cable drops in
    c = to_world(c)
    # same joint as the original cup: a stub along the back plate to the seam, and the key block
    stub = Box(H.WALL + 6, H.WALL, H.z_top - H.tray_bot, align=(Align.MAX, Align.MIN, Align.MIN)).moved(
        Location((x_seam, H.y_back, H.tray_bot)))
    return c + stub + H.joint_block(x_seam, -1, hang=True)


def overlap(a, b):
    o = a & b
    return 0.0 if o is None else o.volume


if __name__ == "__main__":
    here = EXPORTS
    c = cup_slim()
    back, front = RS.shells()
    inn = RS.internals()
    remote = to_world(Part() + [back, front, inn["strips"], inn["boot"]])
    bb, rb = c.bounding_box(), remote.bounding_box()
    print(f"cup_slim {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm, {c.volume / 1000:.1f} cm^3")
    print(f"remote vs cup {overlap(remote, c):.2f} mm^3, cup vs stop (11 mm sleeve) "
          f"{overlap(c, H.stop_keepout(11.0)):.2f}, remote vs stop {overlap(remote, H.stop_keepout(11.0)):.2f} (want 0)")
    rim = H.tray_bot + H.WALL + DEPTH
    print(f"rim {rim - H.tray_bot:.1f} above the cup bottom (the joint stub runs up to the plate top); "
          f"remote stands {rb.max.Z - rim:.1f} above the rim; "
          f"boot hangs {H.tray_bot - rb.min.Z:.1f} below the cup")
    export("cup_slim", c, here)

    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    cx = x_seam - RS.W / 2 - CLR - H.WALL
    fig, axs = plt.subplots(1, 3, figsize=(16, 7), gridspec_kw={"width_ratios": [1.3, 1.3, 0.8]})
    for ax, pl, ix, t in [(axs[0], Plane.XZ.offset(-(H.y_plate + CLR + RS.SEAM)), "X", "face-on (from the room), through the cable"),
                          (axs[2], Plane.YZ.offset(cx), "Y", "edge-on (room to the right)")]:
        for shape, col in [(c, "#cfc6b4"), (remote, "#444")]:
            sec = shape & pl
            if sec is None:
                continue
            for f in sec.faces():
                for w in [f.outer_wire()] + f.inner_wires():
                    pts = [w.position_at(i / 300) for i in range(301)]
                    ax.fill([getattr(p, ix) for p in pts], [p.Z for p in pts], color=col, edgecolor="k", lw=.5)
        ax.set_aspect("equal"); ax.set_title(t, fontsize=10)
    axs[1].imshow(RS.shade([(c, (0.80, 0.77, 0.70)), (remote, (0.33, 0.34, 0.36))], 20, 60))
    axs[1].set_axis_off(); axs[1].set_title("docked", fontsize=10)
    fig.suptitle("Slim remote in cup_slim.stl")
    fig.savefig(here / "remote_slim_fit.png", dpi=95, bbox_inches="tight")
