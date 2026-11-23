"""The whole thing on the mattress stop, for the top of the README: exports/preview.png.

    uv run python cad/preview.py

Two views: from the room (strip and cup) and from behind (the stop, the saddle's lip and the tail's
gusset). The stop is the modelled keep-out with a 12 mm sleeve, not a measured part.
"""
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import holder as H  # noqa: E402
import holder_mag as M  # noqa: E402
import holder_side as HS  # noqa: E402
import remote_shell as RS  # noqa: E402

EXPORTS = pathlib.Path(__file__).parent.parent / "exports"

b = HS.build()
parts = [
    (H.stop_keepout(12.0), (0.55, 0.55, 0.55)),      # the mattress stop, cloth sleeve on
    (b["saddle"], (0.85, 0.78, 0.62)),
    (b["tail"], (0.55, 0.68, 0.85)),
    (b["cup"], (0.80, 0.66, 0.50)),
    (M.insert(), (0.70, 0.80, 0.60)),
    (b["strip"], (0.95, 0.95, 0.93)),
] + [(k, (0.90, 0.45, 0.35)) for k in b["keys"]] + [(a, (0.35, 0.35, 0.40)) for a in b["adapters"]]

fig, axs = plt.subplots(1, 2, figsize=(16, 6))
for ax, (title, elev, azim) in zip(axs, [("from the room", 25, 60), ("from behind", 25, 240)]):
    ax.imshow(RS.shade(parts, elev, azim, px=900))
    ax.set_axis_off()
    ax.set_title(title, fontsize=11, color="#555")
fig.suptitle("Power strip and remote holder on the mattress stop", fontsize=14)
EXPORTS.mkdir(exist_ok=True)
fig.savefig(EXPORTS / "preview.png", dpi=90, bbox_inches="tight", facecolor="white")
print(f"wrote {EXPORTS / 'preview.png'}")
