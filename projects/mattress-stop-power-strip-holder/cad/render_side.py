"""Variant B renders: side_profile.png (sections through an adapter and through a socket),
side_front.png (from the room), adapter.png (the bayonet: inserting vs locked, and the part)."""
import pathlib
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from build123d import Plane, Location
import holder as H, holder_mag as M, holder_side as B, strip as S, adapter as A
here = pathlib.Path(__file__).parent.parent / "exports"
b = B.build()
s, ins, strip, ads = b["saddle"], M.insert(), b["strip"], b["adapters"]
r = H.SLEEVE_D / 2
x_far, x_cord = [B.strip_x0 + S.LENGTH / 2 + x for x in S.plus_xs()]
x_sock = B.strip_x0 + S.LENGTH / 2 + S.socket_xs()[1]


def fill(ax, faces, col, ix, iy, **kw):
    for f in faces:
        for w in [f.outer_wire()] + f.inner_wires():
            pts = [w.position_at(i / 300) for i in range(301)]
            ax.fill([getattr(p, ix) for p in pts], [getattr(p, iy) for p in pts], color=col, edgecolor="k", lw=.5, **kw)


fig, axs = plt.subplots(1, 2, figsize=(13, 6))
for ax, x, t in [(axs[0], x_far, "section through the far-end adapter"), (axs[1], x_sock, "section through a socket")]:
    ax.add_patch(plt.Rectangle((-H.SLEEVE_D, -H.PANEL_H), H.SLEEVE_D, H.PANEL_H - r, color="#e6dcc6"))
    ax.add_patch(plt.Circle((-r, -r), r, color="#d9cfb8")); ax.add_patch(plt.Circle((-r, -r), 4, color="#999"))
    pl = Plane.YZ.offset(x)
    fill(ax, (ins & pl).faces(), "#9dbbd6", "Y", "Z")
    fill(ax, (s & pl).faces(), "#cfc6b4", "Y", "Z")
    fill(ax, (strip & pl).faces(), "#f4f4f4", "Y", "Z")
    for a in ads:
        fill(ax, (a & pl).faces(), "#e07b39", "Y", "Z")
    ax.text(-30, 9, "mattress side", fontsize=9); ax.text(30, 9, "room side", fontsize=9)
    ax.set_aspect("equal"); ax.set_title(t); ax.set_xlim(-35, 75); ax.set_ylim(-60, 15)
fig.suptitle(f"Variant B: Elworks 6-way ({S.LENGTH:.0f} x {S.WIDTH} x {S.HEIGHT}) on its side, sockets to the room; "
             "adapter feet (orange) in vertical T-slots")
fig.savefig(here / "side_profile.png", dpi=105, bbox_inches="tight")

# from the room: the holder, the strip outline with sockets, plus holes and adapters
fig, ax = plt.subplots(figsize=(16, 3.6))
for p, col in zip([s, b["tail"], b["cup"]], ["#cfc6b4", "#c6d3dc", "#ddd"]):
    bb = p.bounding_box()
    ax.add_patch(plt.Rectangle((bb.min.X, bb.min.Z), bb.size.X, bb.size.Z, fc=col, ec="k", lw=.5))
pl = Plane.XZ.offset(-(B.y_strip + 1))
fill(ax, (strip & pl).faces(), "#f7f7f7", "X", "Z")
for xc in S.socket_xs():
    ax.add_patch(plt.Circle((B.strip_x0 + S.LENGTH / 2 + xc, B.z_mid), S.SOCKET_D / 2, fc="none", ec="#999", ls="--"))
for a in ads:
    fill(ax, (a & Plane.XZ.offset(-(B.y_strip - 1))).faces(), "#e07b39", "X", "Z", alpha=.9)
ax.annotate("cord", (B.strip_x0 + S.LENGTH + 12, B.z_mid), fontsize=9)
ax.set_aspect("equal"); ax.set_xlim(-160, 330); ax.set_ylim(-58, 8)
ax.invert_xaxis()   # seen from the room, +X (the cord end) is on the left
ax.set_title("from the room: cord on the left, remote cup on the right. Beige saddle, blue tail, "
             "grey cup; orange = adapter feet at the plus holes; dashed = sockets", fontsize=9)
fig.savefig(here / "side_front.png", dpi=105, bbox_inches="tight")

# the bayonet
fig, axs = plt.subplots(1, 3, figsize=(13, 4.3))
for ax, ang, t in [(axs[0], 0, "inserting: head lines up with the plus"), (axs[1], 45, "turned 45 deg: locked")]:
    fill(ax, S.plus_sketch().faces(), "#666", "X", "Y", alpha=.35)
    ax.add_patch(plt.Rectangle((-S.POCKET_W / 2, -S.POCKET_W / 2), S.POCKET_W, S.POCKET_W, fc="none", ec="#999", ls="--"))
    fill(ax, A.head_sketch(ang).faces(), "#e07b39", "X", "Y", alpha=.6)
    ax.set_aspect("equal"); ax.set_xlim(-7, 7); ax.set_ylim(-7, 7); ax.set_title(t, fontsize=10)
axs[1].text(-6.8, -6.8, f"behind the wall: {A.bearing_area():.1f} mm^2", fontsize=9)
a = A.adapter()
base = S.plus_cavity()
fill(axs[2], (a & Plane.XZ).faces(), "#e07b39", "X", "Z")
from build123d import Box, Align
blk = Box(30, 30, 7, align=(Align.CENTER, Align.CENTER, Align.MIN)) - base
fill(axs[2], (blk & Plane.XZ).faces(), "#eee", "X", "Z", alpha=.8)
axs[2].axhline(0, color="#c96", lw=.8); axs[2].text(-14, -0.9, "rail front face = strip's back", fontsize=7)
axs[2].set_aspect("equal"); axs[2].set_xlim(-15, 15); axs[2].set_ylim(-6, 8)
axs[2].set_title("adapter section (strip base above, rail lips below the line)", fontsize=10)
fig.savefig(here / "adapter.png", dpi=105, bbox_inches="tight")
