"""How the latch works: plan view of the pawls, and a side view of each tooth against its slot wall.

    uv run python cad/latch_picture.py      # writes exports/latch_mechanism.png

Left: seen from the cushion side, looking down on the hooks (the plate's CAD frame). Right: the arc through
each tooth rolled out flat, the cushion's face drawn at drop-on and at home.
"""
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle, Wedge
from shapely.geometry import Polygon as Shape

from workshop.measure import dims

import dyson_half as dl
import hooks
import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
RED, BLUE, GREY = "#d62728", "#1f77b4", "#9aa5b1"


def band(ax, r0, r1, a0, a1, **kw):
    ax.add_patch(Wedge((0, 0), r1, a0, a1, width=r1 - r0, **kw))


def outline_polygon():
    """The plate's nominal outline (before the edge chamfer and fillet) as a shapely polygon."""
    wire = dl.outline().faces()[0].outer_wire()
    return Shape([(p.X, p.Y) for p in wire.positions([i / 4000 for i in range(4000)])])


def plan(ax):
    twist = dim("TWIST_TRAVEL_DEG")
    ax.add_patch(Polygon(list(outline_polygon().exterior.coords), fc="#e9e9e9", ec="#444", lw=1.5))
    ax.add_patch(Circle((0, 0), dim("BORE_DIAMETER") / 2, fc="white", ec="#444", lw=1))
    ax.add_patch(Circle((0, 0), dim("STEM_OUTER_RADIUS"), fc="none", ec="#888", lw=1, ls=":"))
    for s, sp, kind in hooks.hook_spans():
        band(ax, dim("STEM_INNER_RADIUS")[kind], dim("LIP_OUTER_RADIUS")[kind], s, s + sp, fc=GREY, ec="#34495e", lw=1)
    r_slot = (dl.SLOT_INNER_RADIUS, dim("SLOT_OPPOSING_SPAN") / 2)
    for name, p in zip("AB", dl.pawls()):
        band(ax, *r_slot, p["wall"] + twist, p["closed"] + twist, fc="none", ec=BLUE, lw=1.4, ls="--", zorder=4)
        band(ax, *r_slot, p["wall"], p["closed"], fc=BLUE, ec="#0b3d63", lw=1, alpha=0.3, zorder=4)
        band(ax, dl.R_IN - dl.SLIT, dl.R_OUT + dl.SLIT, p["root"], p["slit_end"], fc="white", ec="none", zorder=5)
        band(ax, dl.R_IN, dl.R_OUT, p["root"] - 0.5, p["narrow_from"], fc="#f4b6b6", ec="none", zorder=6)
        band(ax, dl.R_TIP, dl.R_OUT, p["narrow_from"], p["tip"], fc="#f4b6b6", ec="none", zorder=6)
        band(ax, dl.R_TIP, dl.R_OUT, p["foot"], p["tip"] - 0.1 * dl.DEG_PER_MM, fc=RED, ec="#7f1d1d", lw=1, zorder=7)
        mid = math.radians((p["root"] + p["foot"]) / 2)
        ax.annotate(f"pawl {name}: spring arm,\ntooth (dark) at its tip", (dl.R_MID * math.cos(mid), dl.R_MID * math.sin(mid)),
                    (27 * math.cos(mid) * 0.75, 27 * math.sin(mid) * 0.75), color=RED, fontsize=9, ha="center", va="center",
                    arrowprops=dict(arrowstyle="-", color=RED), zorder=8)
        a = math.radians((p["wall"] + p["closed"]) / 2 + 4)
        ax.text(44.5 * math.cos(a), 44.5 * math.sin(a), "short slot\n(home)", color="#0b3d63", fontsize=8, ha="center", va="center")
    p = dl.pawls()[0]
    arc = [(43 * math.cos(math.radians(a)), 43 * math.sin(math.radians(a))) for a in (p["closed"] + twist, p["closed"] + 2)]
    ax.annotate("", xy=arc[1], xytext=arc[0], arrowprops=dict(arrowstyle="->", color=BLUE, lw=2, connectionstyle="arc3,rad=-0.15"))
    ax.set_title("Plan view from the cushion side", fontsize=11)
    ax.text(0, -52, "blue = the cushion's short slots at home; dashed = at drop-on (16° back); arrow = twist to lock\n"
            "pink = spring arm (cut free by the white slit), dark red = tooth; grey = hooks; dotted = seat edge",
            ha="center", va="top", fontsize=8.5)
    ax.set_xlim(-56, 56); ax.set_ylim(-58, 52); ax.set_aspect("equal"); ax.axis("off")


def side(ax, name, p):
    """Unrolled: x = mm along the arc from the tooth's lock-face foot (+ towards the hook), y = height."""
    t, h, twist = dl.T_PLATE, dim("LATCH_TOOTH_HEIGHT"), dim("TWIST_TRAVEL_DEG")
    prof = dl.tooth_profile()
    tip = prof[-1][0] + 0.1
    wall = (p["wall"] - p["foot"]) / dl.DEG_PER_MM              # slot wall at nominal home, mm from the foot
    root = -dim("LATCH_ARM_LENGTH_DEG") / dl.DEG_PER_MM
    x0, x1 = -9.0, 7.5
    ax.add_patch(Rectangle((x0, -2.0), x1 - x0, 2.0, fc="#dfe6ee", ec="#445", lw=0.8))                    # Bose half
    ax.add_patch(Rectangle((x0, -dim("BOSE_LATCH_POCKET_DEPTH")), tip + dl.SLIT + 0.4 - x0, dim("BOSE_LATCH_POCKET_DEPTH"),
                           fc="white", ec="#445", lw=0.8))                                                # its pocket
    ax.add_patch(Rectangle((tip + dl.SLIT, 0), x1 - tip - dl.SLIT, t, fc="#e9e9e9", ec="#444", lw=0.8))   # seat past the slit
    ax.add_patch(Polygon([(x0, 0), (tip, 0), (tip, dl.Z_ARM)] + prof[::-1] + [(x0, dl.Z_ARM)], fc="#f4b6b6", ec="#7f1d1d", lw=1))
    ax.add_patch(Polygon(prof, fc=RED, ec="#7f1d1d", lw=1))
    # the cushion's face: solid on the left of the wall, slot on the right. Home (solid) and drop-on (dashed)
    ax.add_patch(Polygon([(x0, t), (wall, t), (wall, t + 2.6), (x0, t + 2.6)], fc=BLUE, ec="#0b3d63", alpha=0.3, lw=1))
    ax.plot([wall, wall], [t, t + 2.6], color="#0b3d63", lw=2)
    drop = wall + twist / dl.DEG_PER_MM
    ax.plot([x0, min(drop, x1)], [t + 0.03] * 2, color=BLUE, lw=1.4, ls="--")
    ax.annotate("cushion face at drop-on:\nover the tooth, pressing it flat", (4.5, t + 0.05), (3.2, t + 1.9), fontsize=8, color=BLUE,
                ha="center", arrowprops=dict(arrowstyle="-", color=BLUE))
    ax.annotate("slot end wall\nat nominal home", (wall, t + 2.3), (wall - 4.2, t + 3.4), fontsize=8, color="#0b3d63", ha="center",
                arrowprops=dict(arrowstyle="-", color="#0b3d63"))
    ax.annotate("", xy=(wall + 0.1, t + 1.5), xytext=(wall + 3.2, t + 1.5), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.6))
    ax.text(-8.6, -0.8, "pocket in the Bose half", fontsize=8, color="#445", va="center")
    ax.text(-8.6, 0.9, f"spring arm (root {dl.dim('LATCH_ARM_LENGTH_DEG') / dl.DEG_PER_MM:.1f} mm to the left)", fontsize=8, color="#7f1d1d", va="center")
    ax.text(x1 - 0.2, 0.9, "seat", fontsize=8, color="#444", va="center", ha="right")
    gap = wall - dim("LATCH_ARM_TOP_BELOW_SEAT") / math.tan(math.radians(dim("LATCH_LOCK_FACE_DEG")))    # wall to the lock face, at the seat plane
    if gap <= 0:
        state = f"wall has cleared the tooth: it is up, {-gap:.2f} mm ({-gap * dl.DEG_PER_MM:.1f}°) of play"
    else:
        state = f"tooth still held flat; it comes up if the cushion twists {gap * dl.DEG_PER_MM:.1f}° further"
    ax.set_title(f"Pawl {name}, side view at nominal home: {state}", fontsize=9.5)
    ax.set_xlim(x0, x1); ax.set_ylim(-2.3, t + 4.3); ax.set_aspect("equal"); ax.axis("off")


def main():
    fig = plt.figure(figsize=(15, 9.5), dpi=110)
    grid = fig.add_gridspec(2, 2, width_ratios=(1.0, 1.15))
    plan(fig.add_subplot(grid[:, 0]))
    for i, (name, p) in enumerate(zip("AB", dl.pawls())):
        side(fig.add_subplot(grid[i, 1]), name, p)
    fig.suptitle("dyson_half: spring pawls that click into the cushion's short slots", fontsize=13)
    fig.savefig(OUT / "latch_mechanism.png", bbox_inches="tight")
    print("wrote", OUT / "latch_mechanism.png")


if __name__ == "__main__":
    main()
