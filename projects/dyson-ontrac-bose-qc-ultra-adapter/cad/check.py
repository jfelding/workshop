"""Checks on the exported parts, and the picture of the glued adapter.

    uv run python cad/check.py             # after dyson_half.py and bose_half.py

Writes exports/checks.json and exports/preview.png. Exits non-zero if a check fails.
"""
import json
import tempfile
from pathlib import Path

import numpy as np
import trimesh

from workshop.cad.preview import preview
from workshop.cad.printability import layers, mesh_check
from workshop.measure import dims

import measurements as m
from dyson_half import pin_positions

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
report = {}

for name in ("dyson_half", "bose_half"):
    stl = OUT / f"{name}.stl"
    mesh = mesh_check(stl)                      # watertight, one part, sitting on the bed
    summary, _ = layers(stl)                    # no layer starts in mid-air
    report[name] = {
        "triangles": mesh["triangles"], "volume_mm3": mesh["signed_volume_mm3"],
        "size_mm": [round(float(v), 2) for v in trimesh.load(stl).extents],
        "first_layer_area_mm2": summary["first_layer_material_area_mm2"],
        "islands_starting_in_mid_air": summary["new_islands_without_previous_layer_overlap"],
        "area_outside_45deg_of_layer_below_mm2": summary["max_area_outside_45deg_layer_envelope_mm2"],
    }

dyson, bose = trimesh.load(OUT / "dyson_half.stl"), trimesh.load(OUT / "bose_half.stl")
# Glued position: the Bose half turned over about Y, its flat back against the Dyson half's.
bose.apply_transform(trimesh.transformations.rotation_matrix(np.pi, (0, 1, 0)))

# The two halves touch on the glue face and nowhere overlap.
overlap = trimesh.boolean.intersection([dyson, bose], engine="manifold").volume
assert overlap < 0.01, overlap

# Outlines flush: the same oval on both sides of the seam.
edge = max(abs(dyson.extents[i] - bose.extents[i]) for i in (0, 1))
assert edge < 0.1, edge

# Each pin has a straight path: through the Dyson hole and into the Bose pocket.
pin_r, depth, thin = 1.75 / 2, dim("PIN_POCKET_DEPTH"), dim("PLATE_THICKNESS") - dim("RELIEF_DEPTH")
pins = []
for x, y in pin_positions():
    pin = trimesh.creation.cylinder(radius=pin_r - 0.02, height=thin + depth - 0.1, sections=48)
    pin.apply_translation((x, y, (thin - depth) / 2))
    hit = sum(trimesh.boolean.intersection([pin, part], engine="manifold").volume for part in (dyson, bose))
    assert hit < 0.01, (x, y, hit)
    pins.append([round(x, 2), round(y, 2)])

report["glued"] = {
    "overlap_volume_mm3": round(float(overlap), 4), "outline_mismatch_mm": round(float(edge), 3),
    "pins_xy_mm": pins, "pin_path_blocked_mm3": 0.0,
    "stack_height_mm": round(float(dyson.bounds[1][2] - bose.bounds[0][2]), 2),
    "seat_to_bose_plate_mm": dim("PLATE_THICKNESS") + dim("BOSE_FRAME_THICKNESS"),
}
(OUT / "checks.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))

with tempfile.TemporaryDirectory() as tmp:      # the whole thing, for the top of the README
    whole = Path(tmp) / "adapter_glued.stl"
    trimesh.util.concatenate([dyson, bose]).export(whole)
    preview(whole, OUT / "preview.png")
