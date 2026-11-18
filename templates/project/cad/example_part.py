"""Example part: a block with a pin bore and a captive M3 nut. Replace it with your own.

    uv run python cad/example_part.py
"""
from pathlib import Path

from workshop.cad.checks import fits_bed, overhangs, probe
from workshop.cad.export import export
from workshop.cad.geometry import box, cylinder, hex_pocket
from workshop.cad.preview import preview
from workshop.fits import hole_for, nut_pocket
from workshop.measure import dims

import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"   # writes .stl, .step and a .png picture
BED = (220, 220, 270)   # Neptune 3 Pro, from equipment/neptune-3-pro

bore = hole_for(dim("SHAFT_DIAMETER"), "running")
af, depth = nut_pocket(dim("NUT_M3_ACROSS_FLATS"), dim("NUT_M3_THICKNESS"), "press")
size = bore + 2 * dim("WALL") + 10

part = box(0, size, 0, size, 0, 12)
part -= hex_pocket(af, depth / 2, "z", (size - 6, size - 6, 12 - depth / 2))
part -= cylinder(bore / 2, 12, "z", (bore / 2 + dim("WALL"), size / 2, 6))   # cut bores last

assert fits_bed(part, BED)
wall = probe(part, (bore / 2 + dim("WALL"), size / 2, 6), (-1, size / 2, 6))   # from the hole outward
print(f"bore {bore} mm, nut pocket {af} AF × {depth}, wall at bore {wall:.2f} mm, "
      f"overhang {overhangs(part)['steeper_than_45_mm2']:.0f} mm²")
stl = export("example_part", part, OUT)
preview(stl, OUT / "preview.png")   # the whole thing, top of the README; for an assembly use export_many
