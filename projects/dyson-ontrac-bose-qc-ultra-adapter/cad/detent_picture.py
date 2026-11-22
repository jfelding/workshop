"""Plan view of the detent test variant: the ledge bars at drop-on and at home, and the bumps.

    uv run python cad/detent_picture.py     # writes exports/dyson_half_detent_mechanism.png

Seen from the cushion side, looking down on the hooks (the plate's CAD frame). The bars are the
photo-read ones: not proven by fit.
"""
import math
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Wedge, Polygon

from workshop.measure import dims

import dyson_half
import dyson_half_wide
import detent_check
import dyson_half_detent as dd
import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"


def band(ax, r0, r1, a0, a1, **kw):
    ax.add_patch(Wedge((0, 0), r1, a0, a1, width=r1 - r0, **kw))


def main():
    twist = dim("TWIST_TRAVEL_DEG")
    fig, ax = plt.subplots(figsize=(9, 11), dpi=110)
    poly = detent_check.outline_polygon()
    ax.add_patch(Polygon(list(poly.exterior.coords), fc="#e9e9e9", ec="#444", lw=1.5))   # the wide plate
    ax.add_patch(Ellipse((0, 0), dim("BOSE_OVAL_X"), dim("BOSE_OVAL_Y"), fc="none", ec="#222", lw=0.8, ls=(0, (6, 4)), zorder=7))
    ax.add_patch(Circle((0, 0), dim("RING_OUTER_RADIUS"), fc="none", ec="#2a9d3a", lw=1.8, zorder=7))
    ax.text(0, dim("RING_OUTER_RADIUS") - 6.5, "", fontsize=1)
    ax.annotate("cushion's hard ring, outer edge\n(radius 41.1 mm, from a photo)", (dim("RING_OUTER_RADIUS") * 0.9, -dim("RING_OUTER_RADIUS") * 0.43),
                (31, -49), color="#1d6f2a", fontsize=8.5, ha="center", arrowprops=dict(arrowstyle="-", color="#2a9d3a"), zorder=8)
    ax.annotate("old oval (Bose outline, 78 mm wide)\ndashed", (-dim("BOSE_OVAL_X") / 2, 8), (-34, 56), color="#222", fontsize=8.5,
                ha="center", arrowprops=dict(arrowstyle="-", color="#222"), zorder=8)
    ax.add_patch(Circle((0, 0), dim("BORE_DIAMETER") / 2, fc="white", ec="#444", lw=1))
    ax.add_patch(Circle((0, 0), dim("STEM_OUTER_RADIUS"), fc="none", ec="#888", lw=1, ls=":"))
    for s, sp, kind in dyson_half.hook_spans():
        band(ax, dim("STEM_INNER_RADIUS")[kind], dim("LIP_OUTER_RADIUS")[kind], s, s + sp, fc="#9aa5b1", ec="#34495e", lw=1)
    crest = dd.bump_crest_deg()
    prof, rel, app = dd.bump_profile()
    r_mid = (dim("BUMP_INNER_RADIUS") + dim("BUMP_OUTER_RADIUS")) / 2
    k = math.degrees(1 / r_mid)
    for a in (crest, crest + 180):
        band(ax, dim("BUMP_INNER_RADIUS"), dim("BUMP_OUTER_RADIUS"), a - (dim("BUMP_CREST_LENGTH") / 2 + rel) * k,
             a + (dim("BUMP_CREST_LENGTH") / 2 + app) * k, fc="#d62728", ec="#7f1d1d", lw=1.2, zorder=5)
        x, y = r_mid * math.cos(math.radians(a)), r_mid * math.sin(math.radians(a))
        ax.annotate("bump", (x, y), (1.32 * x, 1.32 * y), color="#d62728", fontsize=11, ha="center",
                    arrowprops=dict(arrowstyle="-", color="#d62728"), zorder=6)
    for kind, lo, hi, r0, r1 in dd.bars_cad():
        band(ax, r0, r1, lo + twist, hi + twist, fc="none", ec="#1f77b4", lw=1.6, ls="--", zorder=4)
        band(ax, r0, r1, lo, hi, fc="#1f77b4", ec="#0b3d63", lw=1, alpha=0.55, zorder=4)
        mid = math.radians((lo + hi) / 2)
        ax.text(31.5 * math.cos(mid), 31.5 * math.sin(mid), f"{kind}\nbar", color="#0b3d63", fontsize=8, ha="center", va="center")
    lo, hi, r0, r1 = dd.long_bar()
    a = math.radians(lo + hi / 2 - lo / 2 + 180)
    ax.annotate("", xy=(44.5 * math.cos(math.radians(hi + 180 - 1)), 44.5 * math.sin(math.radians(hi + 180 - 1))),
                xytext=(44.5 * math.cos(math.radians(hi + 180 + twist - 2)), 44.5 * math.sin(math.radians(hi + 180 + twist - 2))),
                arrowprops=dict(arrowstyle="->", color="#1f77b4", lw=2))
    ax.text(0, -55.5, "solid blue = ledge bars at home;  dashed = at drop-on (16 degrees back);  arrow = bars' motion while twisting\n"
            "red = bump on the relief step (0.4 mm high; the bar clears the relief by 0.2 mm);  grey = hooks, dotted = seat edge\n"
            "bars, angles and the ring radius are read from a photo, not proven by fit.   Bumps only under the two long bars.\n"
            "Wide plate: bulges 2.5 mm past the old oval at the sides so the green ring is covered all round.",
            ha="center", va="top", fontsize=8.5)
    ax.set_title("dyson_half_detent on the wide plate: ledge bars (blue), bumps (red), cushion ring (green), plan view", fontsize=11)
    ax.set_xlim(-46, 46); ax.set_ylim(-60, 60); ax.set_aspect("equal"); ax.axis("off")
    fig.savefig(OUT / "dyson_half_detent_mechanism.png", bbox_inches="tight")
    print("wrote", OUT / "dyson_half_detent_mechanism.png")


if __name__ == "__main__":
    main()
