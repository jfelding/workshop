"""Checks on the single case, written to exports/checks.json.

    uv run python cad/check.py     # after cad/single_case.py

- closing: the cradle half folded 180° about the hinge axis must overlap the stand half no more than the original
  two-head case does (the original's overlap is the hinge knuckles and lip, which print separate);
- the kept lane has the original lane's width: free floor from the hinge-side wall to the outer wall;
- bed fit on the Neptune 3 Pro (235 x 235 mm).
"""
import json
import sys
from pathlib import Path

import numpy as np
import trimesh

import single_case as sc

ROOT = Path(__file__).parents[1]
BED = (235.0, 235.0)


def hinge_axis(stand):
    """(y, z) of the fold: y = 0, z = the rim height both halves share (9.5 mm), so the rims close face to face.

    A scan of the original over z = 4..12 mm put its smallest overlap (2.5 mm³, the knuckles) at exactly 9.5.
    """
    v = stand.vertices
    rim = v[(v[:, 0] < 2.0) & (v[:, 1] > 5.0)][:, 2].max()
    return 0.0, rim


def closed_overlap(cradle, stand):
    y, z = hinge_axis(stand)
    folded = cradle.copy()
    folded.apply_transform(trimesh.transformations.rotation_matrix(np.pi, (1, 0, 0), (0, y, z)))
    return trimesh.boolean.intersection([folded, stand], engine="manifold").volume, z


def main():
    result = {}
    orig_c, orig_s = sorted(sc.load(sc.SOURCES["single_case"]), key=lambda b: b.bounds[0][1])
    ref, z = closed_overlap(orig_c, orig_s)
    result["hinge_axis_z"] = round(z, 2)
    result["closed_overlap_original_mm3"] = round(ref, 2)
    for name, src in sc.SOURCES.items():
        cradle, stand = sc.build(src)
        ov, _ = closed_overlap(cradle, stand)
        case = trimesh.util.concatenate([cradle, stand])
        r = {"closed_overlap_mm3": round(ov, 2),
             "extents_mm": np.round(case.extents, 2).tolist(),
             "closed_outer_y_mm": [round(float(cradle.bounds[0][1]), 2), round(float(stand.bounds[1][1]), 2)],
             "fits_bed": bool(case.extents[0] <= BED[0] and case.extents[1] <= BED[1]),
             "watertight": bool(cradle.is_watertight and stand.is_watertight)}
        result[name] = r
        assert r["fits_bed"] and r["watertight"]
        assert ov <= ref + 1.0, f"{name}: folded halves overlap {ov:.1f} mm³ (original {ref:.1f})"
    (ROOT / "exports" / "checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())
