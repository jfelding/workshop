"""Checks on the detent test variant: a motion sweep of the ledge bars over the plate, slack, containment.

    uv run python cad/detent_check.py       # after dyson_half_detent.py; check.py also calls run()

The ledge bars are modelled as simple solids (annular sectors from the photo-read angles and radii) that
stand LEDGE_PROTRUSION proud of the cushion face, so with the cushion fully seated their underside is
0.2 mm above the relief surface. They are turned through the twist from drop-on to home; "offset" is the
degrees still to go to home. Asserts what must hold; reports what is a finding.
"""
import math
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import Polygon

from workshop.measure import dims

import dyson_half
import dyson_half_detent as dd
import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
Z_BAR0 = dd.T_PLATE - dim("LEDGE_PROTRUSION")     # underside of a bar when the cushion is seated
ELLIPSE = (dim("BOSE_OVAL_X") / 2, dim("BOSE_OVAL_Y") / 2)


def sector(lo, hi, r0, r1):
    n = max(8, int(abs(hi - lo)) * 2)
    outer = [(r1 * math.cos(math.radians(a)), r1 * math.sin(math.radians(a))) for a in np.linspace(lo, hi, n)]
    inner = [(r0 * math.cos(math.radians(a)), r0 * math.sin(math.radians(a))) for a in np.linspace(hi, lo, n)]
    mesh = trimesh.creation.extrude_polygon(Polygon(outer + inner), dd.T_PLATE - Z_BAR0)
    mesh.apply_translation((0, 0, Z_BAR0))
    return mesh


def overlap(bar, part):
    """(volume mm3, depth mm above the bar underside) of the bar's overlap with a part."""
    hit = trimesh.boolean.intersection([bar, part], engine="manifold")
    if hit.is_empty or hit.volume < 1e-6:
        return 0.0, 0.0
    return float(hit.volume), float(hit.bounds[1][2] - Z_BAR0)


def wedge_slack(offset):
    """Axial room (mm) the cushion has to lift at this offset, from the long hook's wedge gap.

    The ledge slab (LEDGE_THICKNESS_ASSUMED) sits between the seat and the lip underside, whose gap runs
    from LIP_GAP_TRAILING at the hook's start to LIP_GAP_LEADING at its end. The bar leads with its `lo`
    end; the narrowest gap it overlaps limits the lift. A bar that has not reached the lip is not limited
    (capped at the leading gap's room).
    """
    start, span, _ = dyson_half.hook_spans()[0]                 # the long hook of slot 0, plate frame
    lo, hi, _, _ = dd.long_bar()
    lo, hi = lo + 180, hi + 180                                # slot 0's own copy of the long bar
    g0, g1 = dim("LIP_GAP_TRAILING"), dim("LIP_GAP_LEADING")
    lead = lo + offset                                         # leading end of the bar
    if lead > start + span:
        return g1 - dim("LEDGE_THICKNESS_ASSUMED")
    gap = g0 + (max(lead, start) - start) / span * (g1 - g0)
    return gap - dim("LEDGE_THICKNESS_ASSUMED")


def run():
    stl = OUT / "dyson_half_detent.stl"
    det, base = trimesh.load(stl), trimesh.load(OUT / "dyson_half.stl")
    twist = dim("TWIST_TRAVEL_DEG")
    bars = dd.bars_cad()
    clearance = Z_BAR0 - dd.Z_RELIEF
    prof, rel, app = dd.bump_profile()
    r_mid = (dim("BUMP_INNER_RADIUS") + dim("BUMP_OUTER_RADIUS")) / 2
    deg_per_mm = math.degrees(1 / r_mid)
    crest = dd.bump_crest_deg()
    lo, hi, r_in, r_out = dd.long_bar()

    # 1. motion sweep, every 0.5 degree from 8 degrees beyond drop-on to home
    rows, other = [], 0.0
    for off in np.arange(twist + 8, -0.01, -0.5):
        row = {"offset_deg": round(float(off), 1)}
        depth_long = 0.0
        for k, (kind, blo, bhi, br0, br1) in enumerate(bars):
            bar = sector(blo + off, bhi + off, br0, br1)
            v_base, _ = overlap(bar, base)
            v_det, d_det = overlap(bar, det)
            other = max(other, v_base)                         # the bars must never touch the proven part
            if kind == "long":
                depth_long = max(depth_long, d_det)
            else:
                other = max(other, v_det)                      # short bars must see no bump at all
        row["bump_interference_mm"] = round(depth_long, 3)
        row["wedge_slack_mm"] = round(float(wedge_slack(off)), 3)
        row["margin_mm"] = round(row["wedge_slack_mm"] - row["bump_interference_mm"], 3)
        rows.append(row)
    assert other < 1e-3, f"a ledge bar touches the plate or the proven features: {other} mm3"

    # 2. drop-on: where would a bar first stand clear of the bump?
    foot_app = crest + (dim("BUMP_CREST_LENGTH") / 2 + app) * deg_per_mm     # high-angle foot
    foot_rel = crest - (dim("BUMP_CREST_LENGTH") / 2 + rel) * deg_per_mm
    twist_to_clear = foot_app - lo                                            # offset where bar's lo end passes the foot
    at_drop = next(r for r in rows if abs(r["offset_deg"] - twist) < 1e-6)
    at_home = rows[-1]

    # 3. containment: bump volume, on the plate, under the bar, clear of the seat
    bump_vol = float(det.volume - base.volume)
    w = dim("BUMP_OUTER_RADIUS") - dim("BUMP_INNER_RADIUS")
    expected = 2 * w * 0.5 * (dim("BUMP_CREST_LENGTH") + (dim("BUMP_CREST_LENGTH") + rel + app)) * dim("BUMP_HEIGHT")
    assert abs(bump_vol - expected) < 0.25 * expected, (bump_vol, expected)
    diff = trimesh.boolean.difference([det, base], engine="manifold")
    pts = diff.vertices
    rr = np.hypot(pts[:, 0], pts[:, 1])
    ang = np.degrees(np.arctan2(pts[:, 1], pts[:, 0]))
    edge = [1 / math.sqrt((p[0] / ELLIPSE[0] / np.hypot(*p[:2])) ** 2 + (p[1] / ELLIPSE[1] / np.hypot(*p[:2])) ** 2) for p in pts]
    plate_margin = float(min(e - r for e, r in zip(edge, rr)))
    assert plate_margin > 1.0, plate_margin                    # edge fillet is 0.6
    assert rr.min() > dim("STEM_OUTER_RADIUS") + 0.5           # clear of the seat's outer edge
    assert rr.min() >= r_in - 0.01 and rr.max() <= r_out + 0.01, (rr.min(), rr.max(), r_in, r_out)
    assert abs(diff.bounds[1][2] - (dd.Z_RELIEF + dim("BUMP_HEIGHT"))) < 0.01
    # no bump lies on a short bar's track or under a hook
    spans = [(s, s + sp) for s, sp, _ in dyson_half.hook_spans()]
    bump_angles = [crest % 360, (crest + 180) % 360]
    near_hook = min(min(abs((a - x + 180) % 360 - 180) for x in (s, e)) for a in bump_angles for s, e in spans)
    # the hook is clear of the whole bump footprint
    hook_gap_deg = min(((foot_app + 180) % 360 - (spans[0][1] % 360)) % 360, 1e9)
    # the plate top under the bump foot is the relief surface: solid just below it, air just above
    foot = trimesh.creation.box((1.0, 0.6, 0.2))
    foot.apply_transform(trimesh.transformations.rotation_matrix(math.radians(crest), (0, 0, 1)))
    c0, s0 = math.cos(math.radians(crest)), math.sin(math.radians(crest))
    below, above = foot.copy(), foot.copy()
    below.apply_translation((r_mid * c0, r_mid * s0, dd.Z_RELIEF - 0.1))
    above.apply_translation((r_mid * c0, r_mid * s0, dd.Z_RELIEF + 0.1 + 0.3))
    assert abs(trimesh.boolean.intersection([below, base], engine="manifold").volume - below.volume) < 1e-3
    assert trimesh.boolean.intersection([above, base], engine="manifold").is_empty

    worst = min(r["margin_mm"] for r in rows if r["offset_deg"] <= twist and r["bump_interference_mm"] > 0)
    peak = max(r["bump_interference_mm"] for r in rows)
    assert abs(peak - (dim("BUMP_HEIGHT") - clearance)) < 0.02, peak        # rises to bump height less the 0.2 clearance
    assert at_home["bump_interference_mm"] == 0.0                           # and is gone again at home
    assert worst >= 0.03, f"bump not passable with margin: {worst}"
    return {
        "bar_home_span_deg_plate_frame": [round(lo, 2), round(hi, 2)], "bar_radii_mm": [r_in, r_out],
        "bump_crest_deg_plate_frame": round(crest, 2),
        "bump_feet_deg": [round(foot_rel, 2), round(foot_app, 2)],
        "bump_ramp_lengths_mm": {"release": round(rel, 2), "approach": round(app, 2)},
        "bump_volume_each_mm3": round(bump_vol / 2, 3),
        "bump_edge_margin_to_plate_outline_mm": round(plate_margin, 2),
        "bump_hook_clearance_deg": round(float(near_hook), 1),
        "bar_clearance_over_relief_mm": round(clearance, 3),
        "peak_interference_mm": peak, "interference_at_home_mm": at_home["bump_interference_mm"],
        "interference_at_drop_on_mm": at_drop["bump_interference_mm"],
        "twist_for_bar_to_clear_bump_deg": round(twist_to_clear, 1),
        "worst_slack_minus_interference_mm": round(float(worst), 3),
        "other_collisions_mm3": round(other, 4),
        "sweep": rows,
    }


if __name__ == "__main__":
    res = run()
    for r in res.pop("sweep"):
        print(r)
    print({k: v for k, v in res.items()})
