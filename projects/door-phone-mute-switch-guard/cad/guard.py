"""Guard cup for the door phone's mute toggle switch, in print orientation (floor on the bed).

The switch's own nut drops into a hex pocket at the bottom of the cup, so the cup is its wrench: turn the
cup by hand and the nut screws down on the floor. The wall stands higher than the lever, so a jacket
brushing past cannot flip it; a pen still can.

    uv run python cad/guard.py      # writes exports/guard.{stl,step,png}, preview.png, checks.json
"""
import json
import math
from pathlib import Path

from build123d import Cone

from workshop.cad.checks import assert_clear, fits_bed, overhangs, probe
from workshop.cad.export import export
from workshop.cad.geometry import cylinder, hex_pocket
from workshop.cad.preview import preview
from workshop.cad.printability import layers, mesh_check
from workshop.fits import hole_for, nut_pocket
from workshop.measure import dims

import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
BED = (220, 220, 270)   # Neptune 3 Pro, from equipment/neptune-3-pro

thread_d = dim("BUSHING_THREAD_DIAMETER")
nut_af, nut_t = dim("NUT_ACROSS_FLATS"), dim("NUT_THICKNESS")
lever_h, lever_span = dim("LEVER_TIP_HEIGHT"), dim("LEVER_SWING_SPAN")
floor, wall, chamfer = dim("FLOOR"), dim("WALL"), dim("RIM_CHAMFER")

hole = hole_for(thread_d, "running")   # the collar passes through freely; the nut does the holding
af, pocket = nut_pocket(nut_af, nut_t, "clearance")   # the nut drops in and is turned by the flats
corner_r = af / math.sqrt(3)
bore_r = max(corner_r, lever_span / 2 + dim("LEVER_CLEARANCE"))   # round bore above the nut, for the lever
ro = bore_r + wall
height = lever_h + dim("RIM_ABOVE_LEVER")

thread_left = dim("THREAD_PAST_NUT") - floor   # thread past the nut once the floor is under it
assert thread_left >= 0, f"the nut runs out of thread by {-thread_left:.2f} mm with a {floor} mm floor under it"

# Hex well for the nut, opening at 45° (no overhang) into the round bore the lever swings in.
z_nut = floor + pocket
z_round = z_nut + (bore_r - af / 2)
assert z_round < height - 1, "the lever is too short for this cup: the bore has not opened up below the rim"
inside = hex_pocket(af, (height - floor) / 2 + 0.01, "z", (0, 0, (height + floor) / 2 + 0.01))
inside += Cone(af / 2, bore_r, z_round - z_nut).translate((0, 0, (z_nut + z_round) / 2))
inside += cylinder(bore_r, height - z_round + 0.02, "z", (0, 0, (height + z_round) / 2 + 0.01))

part = cylinder(ro, height, "z", (0, 0, height / 2))
part -= cylinder(ro + 1, 2 * chamfer, "z", (0, 0, height)) - Cone(ro, ro - 2 * chamfer, 2 * chamfer).translate((0, 0, height))
part -= inside
part -= cylinder(hole / 2, 3 * floor, "z", (0, 0, 0))   # bores last

# --- against the solid: the switch as keep-outs ----------------------------------------
collar_top = floor + nut_t + thread_left
collar = cylinder(thread_d / 2, collar_top, "z", (0, 0, collar_top / 2))
nut = hex_pocket(nut_af, nut_t / 2, "z", (0, 0, floor + nut_t / 2))
# The lever pivots inside the collar, so its swing is a cone: collar-wide where it leaves, full span at the tip.
lever = Cone(thread_d / 2, lever_span / 2, lever_h - collar_top).translate((0, 0, (lever_h + collar_top) / 2))
assert_clear([("collar", part, collar), ("nut", part, nut), ("lever swing", part, lever)])
assert fits_bed(part, BED)

top = (z_round + height) / 2
z_mid = floor + nut_t / 2
report = {
    "size_mm": {"outer_diameter": round(2 * ro, 2), "bore_diameter": round(2 * bore_r, 2), "height": round(height, 2),
                "collar_hole": hole, "nut_well_across_flats": af},
    "probes_mm": {
        "wall, round bore": round(probe(part, (bore_r - 0.2, 0, top), (ro + 1, 0, top)), 2),
        "wall, thinnest around the nut well": round(min(
            probe(part, (0, 0, z_mid), (math.cos(a) * (ro + 1), math.sin(a) * (ro + 1), z_mid))
            for a in (0, math.pi / 6)), 2),
        "floor under the nut": round(probe(part, ((hole + af) / 4, 0, floor + 0.2), ((hole + af) / 4, 0, -1)), 2),
        "floor ring width under the nut flats": round((af - hole) / 2, 2),
    },
    "clearances_mm": {
        "nut in its well, across flats": round(af - nut_af, 2),
        "lever swing to bore, per side": round(bore_r - lever_span / 2, 2),
        "lever tip below rim": round(height - lever_h, 2),
        "thread past the nut": round(thread_left, 2),
    },
    "overhang_mm2": overhangs(part),
}

stl = export("guard", part, OUT)
report["mesh"] = mesh_check(stl)
report["layers"] = layers(stl)[0]
preview(stl, OUT / "preview.png")   # one part, so the whole thing is the part
(OUT / "checks.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
