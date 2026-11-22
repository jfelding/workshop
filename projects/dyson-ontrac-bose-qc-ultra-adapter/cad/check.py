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
import detent_check
from dyson_half import pin_positions

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
report = {}

for name in ("dyson_half", "dyson_half_wide", "dyson_half_detent", "bose_half", "bose_half_wide"):
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

def glue(dyson_name, bose_name):
    """The glued pair: the Bose half turned over about Y, its flat back against the Dyson half's."""
    dyson, bose = trimesh.load(OUT / f"{dyson_name}.stl"), trimesh.load(OUT / f"{bose_name}.stl")
    bose.apply_transform(trimesh.transformations.rotation_matrix(np.pi, (0, 1, 0)))
    # The two halves touch on the glue face and nowhere overlap.
    overlap = trimesh.boolean.intersection([dyson, bose], engine="manifold").volume
    assert overlap < 0.01, overlap
    # Outlines flush: the same outline on both sides of the seam.
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
    info = {
        "overlap_volume_mm3": round(float(overlap), 4), "outline_mismatch_mm": round(float(edge), 3),
        "pins_xy_mm": pins, "pin_path_blocked_mm3": 0.0,
        "stack_height_mm": round(float(dyson.bounds[1][2] - bose.bounds[0][2]), 2),
        "seat_to_bose_plate_mm": dim("PLATE_THICKNESS") + dim("BOSE_FRAME_THICKNESS"),
    }
    return info, dyson, bose


report["glued"], dyson, bose = glue("dyson_half", "bose_half")
report["glued_wide"], dyson_w, bose_w = glue("dyson_half_wide", "bose_half_wide")
# The bulge lands on the same sides on both halves once glued: compare the outlines at the seam, by area.
left = lambda mesh: (float(-mesh.vertices[:, 0].min()), float(mesh.vertices[:, 0].max()))
report["glued_wide"]["bulge_extent_x_dyson_mm"] = [round(v, 2) for v in left(dyson_w)]
report["glued_wide"]["bulge_extent_x_bose_mm"] = [round(v, 2) for v in left(bose_w)]
assert max(abs(p - q) for p, q in zip(left(dyson_w), left(bose_w))) < 0.1

# bose_half_wide against the proven bose_half: nothing removed anywhere, nothing changed inside the oval
narrow, wide = trimesh.load(OUT / "bose_half.stl"), trimesh.load(OUT / "bose_half_wide.stl")
removed = trimesh.boolean.difference([narrow, wide], engine="manifold").volume
from shapely import affinity
from shapely.geometry import Point
inside = trimesh.creation.extrude_polygon(
    affinity.scale(Point(0, 0).buffer(1, resolution=256), dim("BOSE_OVAL_X") / 2 - 0.5, dim("BOSE_OVAL_Y") / 2 - 0.5), 6.0)
added_inside = trimesh.boolean.intersection([trimesh.boolean.difference([wide, narrow], engine="manifold"), inside],
                                            engine="manifold").volume
assert removed < 0.01 and added_inside < 0.01, (removed, added_inside)
report["bose_half_wide"].update({
    "volume_added_vs_proven_bose_half_mm3": round(float(wide.volume - narrow.volume), 3),
    "proven_material_removed_mm3": round(float(removed), 4),
    "added_inside_oval_less_0.5mm_mm3": round(float(added_inside), 4)})
# The detent test variant: the proven part is unchanged and the bump motion sweep (see detent_check.py).
assert abs(report["dyson_half"]["volume_mm3"] - 4885.608) < 0.01, report["dyson_half"]["volume_mm3"]
# The wide plate: same hooks (everything above the seat top is identical), the bumps added on top of it.
above = trimesh.creation.box((120, 120, 10)); above.apply_translation((0, 0, 2.0 + 5))   # z >= 2.0 (seat top)
tops = {n: trimesh.boolean.intersection([trimesh.load(OUT / f"{n}.stl"), above], engine="manifold").volume
        for n in ("dyson_half", "dyson_half_wide")}
assert abs(tops["dyson_half"] - tops["dyson_half_wide"]) < 0.01, tops
report["dyson_half_wide"]["volume_above_seat_matches_proven_mm3"] = round(float(tops["dyson_half"]), 3)
report["dyson_half_wide"]["extra_volume_vs_proven_mm3"] = round(
    report["dyson_half_wide"]["volume_mm3"] - report["dyson_half"]["volume_mm3"], 3)
report["dyson_half_detent"]["bump_volume_added_mm3"] = round(
    report["dyson_half_detent"]["volume_mm3"] - report["dyson_half_wide"]["volume_mm3"], 3)
report["detent_sweep"] = detent_check.run()
(OUT / "checks.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))

with tempfile.TemporaryDirectory() as tmp:      # the whole thing, for the top of the README
    whole = Path(tmp) / "adapter_glued.stl"
    trimesh.util.concatenate([dyson, bose]).export(whole)
    preview(whole, OUT / "preview.png")

with tempfile.TemporaryDirectory() as tmp:      # the wide test pair, kept apart from the published preview
    whole = Path(tmp) / "adapter_glued_wide.stl"
    trimesh.util.concatenate([dyson_w, bose_w]).export(whole)
    preview(whole, OUT / "preview_wide.png")
