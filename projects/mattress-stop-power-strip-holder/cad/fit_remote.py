"""Drop the DewertOkin CLASSIC STEP into the cup (cable end down), check the fit, and draw
sections of it (remote_fit.png)."""
import pathlib
from build123d import *
from workshop.cad.export import export

EXPORTS = pathlib.Path(__file__).parent.parent / "exports"
import holder as H
here = pathlib.Path(__file__).parent
r = import_step(str(here.parent / "vendor" / "dewertokin-classic" / "CLASSIC_6_keys.STEP"))
# STEP: long axis Z (button end at 0, cable end at +Z), width X, thickness Y (keypad +Y).
# Keep the body and the 29 mm strain-relief boot (Z < 168.5); drop the bare cable beyond it and
# the separate hanging bracket modelled behind the back (Y < -9.6).
r = r & Box(60, 30, 168.5, align=(Align.CENTER, Align.MIN, Align.MIN)).moved(Location((0, -9.6, -1)))
r = r.rotate(Axis.Y, 180)   # cable end down, width along X, keypad still towards the room (+Y)
bb = r.bounding_box()
h = H.SADDLE_L / 2
c = H.cup(-h)
cw, ct = H.REMOTE_W + H.CUP_CLR, H.REMOTE_T + H.CUP_CLR
cx, cy = -h - cw / 2 - H.WALL, H.y_plate + ct / 2
body = r
bbody = body.bounding_box()
# rest the curved end on the U floor: lower it until it touches, 0.2 mm steps
r = body.moved(Location((cx - (bbody.min.X + bbody.max.X) / 2, cy - (bbody.min.Y + bbody.max.Y) / 2,
                      H.tray_bot + H.WALL + 40 - bbody.min.Z)))
for dz in [i * 0.2 for i in range(400)]:
    t = r.moved(Location((0, 0, -dz)))
    hit = t & c
    if hit is not None and hit.volume > 1.0:
        r = r.moved(Location((0, 0, -(dz - 0.2))))
        break
b = r.bounding_box()
print(f"remote body seated: lowest point {b.min.Z - H.tray_bot - H.WALL:.1f} mm above the cup floor top, "
      f"{b.max.Z - (H.tray_bot + H.CUP_DEPTH):.1f} mm stands above the cup rim")
o = r & c
print(f"boot tip {b.min.Z - H.tray_bot:.1f} mm relative to the cup's underside; width along X {b.size.X:.1f}, thickness along Y {b.size.Y:.1f}")
print(f"overlap with cup {0 if o is None else o.volume:.2f} mm^3")

# sections through the cup with the seated remote
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, axs = plt.subplots(1, 2, figsize=(11, 7))
for ax, pl, ix, t in [(axs[0], Plane.XZ.offset(-cy), 0, "face-on (from the room)"),
                      (axs[1], Plane.YZ.offset(cx), 1, "edge-on (room to the right)")]:
    for shape, col in [(c, "#cfc6b4"), (r, "#333333")]:
        sec = shape & pl
        if sec is None:
            continue
        for f in sec.faces():
            for w in [f.outer_wire()] + f.inner_wires():
                pts = [tuple(w.position_at(i / 300)) for i in range(301)]
                ax.fill([p[ix] for p in pts], [p[2] for p in pts], color=col, edgecolor="k", lw=.5, alpha=.9)
    ax.set_aspect("equal"); ax.set_title(t)
fig.suptitle("DewertOkin CLASSIC remote (official STEP) seated in the cup")
fig.savefig(EXPORTS / "remote_fit.png", dpi=100, bbox_inches="tight")
