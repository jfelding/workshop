"""Stepped plug gauge for the black pump's (pump C) collar: finds the diameter inside its threads.

Calipers cannot reach inside the collar. Push the collar down over this gauge, smallest step first.
The last step it slides over, measured afterwards with calipers on the print itself, is the size a
plain spigot or a thread crest has to be. The pump's body passes through the bore.

    uv run python cad/pump_c_gauge.py
"""
from pathlib import Path

from workshop.cad.checks import fits_bed, overhangs, probe
from workshop.cad.export import export
from workshop.cad.geometry import cylinder
from workshop.measure import dims

import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
BED = (220, 220, 270)   # Neptune 3 Pro, from equipment/neptune-3-pro

steps = sorted(dim("GAUGE_STEP_DIAMETERS"), reverse=True)   # widest on the bed, so nothing overhangs
h = dim("GAUGE_STEP_HEIGHT")
bore = min(steps) - 2 * dim("GAUGE_WALL")
assert bore > dim("PUMP_C_BODY_OD") + 2, "the pump body must drop through the gauge"
assert len(steps) * h > dim("PUMP_C_COLLAR_DEPTH"), "gauge shorter than the collar is deep"

part = None
for i, d in enumerate(steps):
    c = cylinder(d / 2, h, "z", (0, 0, h * (i + 0.5)))
    part = c if part is None else part + c
part -= cylinder(bore / 2, len(steps) * h + 2, "z", (0, 0, len(steps) * h / 2))   # cut bores last

assert fits_bed(part, BED)
top = len(steps) * h - h / 2
wall = probe(part, (0, 0, top), (min(steps), 0, top))
print(f"steps {steps} mm, bore {bore:.1f} mm, thinnest wall {wall:.2f} mm, overhangs {overhangs(part)}")
export("pump_c_gauge", part, OUT)
