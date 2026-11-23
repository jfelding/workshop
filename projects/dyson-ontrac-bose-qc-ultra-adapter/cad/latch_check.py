"""Checks on the latch: the arms are free, the teeth meet the cushion as intended, the pocket is right.

    uv run python cad/latch_check.py        # after dyson_half.py and bose_half.py; check.py calls run()

The cushion is modelled as the solid part of its hard face next to each short slot: a slab from the seat plane
up, ending at the slot's open-end wall, turned through the twist. "offset" is the degrees still to go to the
nominal home (negative = twisted past it; the hooks hit the slot's closed end at about -2.3). Where the slab
overlaps a tooth, the overlap height is how far that pawl is pushed down. Asserts what must hold; reports the rest.
"""
import math
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import Polygon

from workshop.measure import dims

import bose_half as bl
import dyson_half as dl
import hooks
import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
H = dim("LATCH_TOOTH_HEIGHT")


def sector(r0, r1, a0, a1, z0, z1):
    n = max(8, int(abs(a1 - a0) * 4))
    arc = lambda r, angles: [(r * math.cos(math.radians(a)), r * math.sin(math.radians(a))) for a in angles]
    mesh = trimesh.creation.extrude_polygon(
        Polygon(arc(r1, np.linspace(a0, a1, n)) + arc(r0, np.linspace(a1, a0, n))), z1 - z0)
    mesh.apply_translation((0, 0, z0))
    return mesh


def common(a, b):
    hit = trimesh.boolean.intersection([a, b], engine="manifold")
    return hit if (not hit.is_empty and hit.volume > 1e-6) else None


def spring():
    """Beam numbers for one arm: a cantilever loaded at the tooth's lock-face crest edge."""
    prof = dl.tooth_profile()
    t, w = dl.Z_ARM, dl.R_OUT - dl.R_IN
    length = (dim("LATCH_ARM_LENGTH_DEG") / dl.DEG_PER_MM) + prof[1][0]
    stiff = dim("PLA_MODULUS_ASSUMED_MPA") * w * t ** 3 / (4 * length ** 3)          # N/mm at the tooth
    force = stiff * H
    past = prof[-1][0] + 0.1 - prof[1][0]                     # arm tip beyond the loaded point, mm
    tip_drop = H + past * 1.5 * H / length                    # the tip goes lower than the tooth: slope there
    lever = (H + t / 2) / length                              # wall force acts above the arm's middle: tips it down
    hold = {}
    for mu in (0.2, 0.3, 0.5):
        a = math.radians(dim("LATCH_LOCK_FACE_DEG")) + math.atan(mu)
        cam = 1 / math.tan(a) if a < math.pi / 2 else 0.0
        hold[f"friction_{mu}"] = round(force / (cam + 1.5 * lever), 1)
    return {"arm_thickness_mm": t, "arm_width_mm": round(w, 2), "arm_length_to_tooth_mm": round(length, 2),
            "stiffness_N_per_mm": round(stiff, 2), "force_to_press_one_tooth_flat_N": round(force, 2),
            "peak_strain_percent": round(150 * t * H / length ** 2, 2),
            "arm_tip_drop_when_flat_mm": round(tip_drop, 2),
            "pocket_depth_minus_tip_drop_mm": round(dim("BOSE_LATCH_POCKET_DEPTH") - tip_drop, 2),
            "untwist_force_at_tooth_N_per_pawl": hold,
            "untwist_torque_both_pawls_Nm_friction_0.3": round(2 * hold["friction_0.3"] * dl.R_MID / 1000, 2)}


def run(glued_bose=None):
    latch, bose = trimesh.load(OUT / "dyson_half.stl"), trimesh.load(OUT / "bose_half.stl")
    wide, bose_wide = bl.to_mesh(dl.plate()), bl.before_pockets()     # the same parts without the latch
    pawls, twist, t_plate = dl.pawls(), dim("TWIST_TRAVEL_DEG"), dl.T_PLATE
    names = "AB"
    res = {"pawls_deg_plate_frame": {}, "spring": spring()}
    assert res["spring"]["pocket_depth_minus_tip_drop_mm"] >= 0.15, res["spring"]
    assert res["spring"]["peak_strain_percent"] <= 1.45, res["spring"]   # only while a tooth is pressed flat

    # 1. the slits are open through the plate, and the arm is the only thing between them
    for n, p in zip(names, pawls):
        for r0, r1 in ((dl.R_IN - dl.SLIT, dl.R_IN), (dl.R_OUT, dl.R_OUT + dl.SLIT)):
            gap = sector(r0 + 0.03, r1 - 0.03, p["root"] + 0.2, p["slit_end"] - 0.2, -0.5, 6)
            assert common(gap, latch) is None, f"slit of pawl {n} is not open"
        end = sector(dl.R_IN - dl.SLIT + 0.03, dl.R_OUT + dl.SLIT - 0.03, p["tip"] + 0.08, p["slit_end"] - 0.08, -0.5, 6)
        assert common(end, latch) is None, f"tip slit of pawl {n} is not open"
        notch = sector(dl.R_IN - dl.SLIT + 0.03, dl.R_TIP - 0.03, p["narrow_from"] + 0.08, p["slit_end"] - 0.08, -0.5, 6)
        assert common(notch, latch) is None, f"narrow tip of pawl {n} is not cut"
        arm = common(sector(dl.R_IN, dl.R_OUT, p["root"], p["tip"], -0.5, 6), latch)
        assert abs(arm.bounds[1][2] - (t_plate + H)) < 0.01 and abs(arm.bounds[0][2]) < 1e-6
        body = common(sector(dl.R_IN, dl.R_OUT, p["root"], p["foot"] - 0.02, -0.5, 6), latch)
        assert abs(body.bounds[1][2] - dl.Z_ARM) < 0.01                        # arm top below the seat
        res["pawls_deg_plate_frame"][n] = {
            "slot_wall_at_home": round(p["wall"], 2), "lock_face_foot": round(p["foot"], 2),
            "crest": [round(v, 2) for v in p["crest"]], "arm_root": round(p["root"], 2),
            "slit_end": round(p["slit_end"], 2), "tooth_volume_mm3": round(float(arm.volume - body.volume
                - common(sector(dl.R_IN, dl.R_OUT, p["foot"] - 0.02, p["tip"], -0.5, dl.Z_ARM), latch).volume), 3)}
    # radial room for the tooth in the slot, and clear of hooks and pins
    spans = [(s, s + sp) for s, sp, _ in hooks.hook_spans()]
    hook_gap = min(abs((e - a + 180) % 360 - 180) for p in pawls for a in (p["lowered_from"], p["slit_end"])
                   for s in spans for e in s)
    pins = [math.degrees(math.atan2(y, x)) for x, y in hooks.pin_positions()]
    res["tooth_to_slot_inner_edge_mm"] = round(dl.R_TIP - dl.SLOT_INNER_RADIUS, 2)
    res["tooth_width_mm"] = round(dl.R_OUT - dl.R_TIP, 2)
    res["tooth_to_slot_outer_edge_mm"] = round(dim("SLOT_OPPOSING_SPAN") / 2 - dl.R_OUT, 2)
    res["nearest_hook_end_deg"] = round(float(hook_gap), 1)
    assert res["tooth_to_slot_inner_edge_mm"] >= 0.5 and hook_gap > 8
    res["seat_ring_left_inside_slit_mm"] = round(dl.R_IN - dl.SLIT - dim("BORE_DIAMETER") / 2, 2)
    # nothing above the seat changed except the teeth; the hooks are those of the plate
    above = trimesh.creation.box((120, 120, 10)); above.apply_translation((0, 0, t_plate + 5 + 1e-4))
    extra = common(latch, above).volume - common(wide, above).volume
    res["volume_above_seat_added_mm3"] = round(float(extra), 3)

    # 2. motion sweep: the cushion's solid face beside each short slot, against the part
    rows = []
    for off in np.arange(twist + 2, -2.51, -0.25):
        row = {"offset_deg": round(float(off), 2)}
        for n, p in zip(names, pawls):
            face = sector(30.0, 41.0, p["wall"] + off - 45, p["wall"] + off, t_plate, t_plate + dim("SLOT_DEPTH"))
            hit = common(face, latch)
            row[f"{n}_pushed_down_mm"] = round(float(hit.bounds[1][2] - t_plate), 3) if hit else 0.0
            assert common(face, wide) is None                 # the face meets nothing but the tooth
        rows.append(row)
    at = lambda off: next(r for r in rows if abs(r["offset_deg"] - off) < 1e-6)
    assert all(abs(at(twist)[f"{n}_pushed_down_mm"] - H) < 0.01 for n in names)    # flat under the face at drop-on
    assert at(0.0)["A_pushed_down_mm"] == 0.0                                    # A is up at nominal home
    assert all(rows[-1][f"{n}_pushed_down_mm"] == 0.0 for n in names)            # both up at the hard stop
    up = {n: [r["offset_deg"] for r in rows if r[f"{n}_pushed_down_mm"] == 0.0] for n in names}
    ramp = {n: [r["offset_deg"] for r in rows if 0 < r[f"{n}_pushed_down_mm"] < H - 0.01] for n in names}
    contact = dim("LATCH_ARM_TOP_BELOW_SEAT") / math.tan(math.radians(dim("LATCH_LOCK_FACE_DEG"))) * dl.DEG_PER_MM   # face at the seat plane
    res["sweep_summary"] = {
        n: {"fully_up_from_offset_deg": max(up[n]), "on_the_lock_face_between_deg": [min(ramp[n]), max(ramp[n])],
            "wall_clears_lock_face_at_offset_deg": round(p["foot"] + contact - p["wall"], 2)}
        for n, p in zip(names, pawls)}
    res["hard_stop_offset_deg"] = round(-math.degrees(dim("LOCK_END_GAP") / ((dim("STEM_INNER_RADIUS")["short"]
                                        + dim("STEM_OUTER_RADIUS")) / 2)), 2)

    # 3. the Bose pocket: roof closed, wall to the opening, clips not undercut, frame otherwise untouched
    depth, mg = dim("BOSE_LATCH_POCKET_DEPTH"), dim("BOSE_LATCH_POCKET_MARGIN")
    removed = trimesh.boolean.difference([bose_wide, bose], engine="manifold")
    assert trimesh.boolean.difference([bose, bose_wide], engine="manifold").volume < 1e-3     # nothing added
    pockets = []
    for n, (tip, main) in zip(names, bl.pocket_spans()):
        r0, r1, a0, a1 = main
        roof_solid, on_roof = 1.0, 0.0
        for q0, q1, b0, b1 in (tip, main):
            roof = sector(q0, q1, b0, b1, depth + 0.02, dim("BOSE_FRAME_THICKNESS") - 0.02)
            roof_solid = min(roof_solid, common(roof, bose).volume / roof.volume)
            clip = common(sector(q0, q1, b0, b1, dim("BOSE_FRAME_THICKNESS") + 0.3, 8), bose)   # above the 0.2 ridge
            on_roof += clip.volume if clip else 0.0
        inner = sector(r0 - 0.6, r0 - 0.02, a0, a1, 0.05, depth)
        inner_solid = common(inner, bose).volume / inner.volume
        outer = sector(r1 + 0.02, r1 + 0.6, tip[2], a1, 0.05, depth)
        outer_solid = common(outer, bose).volume / outer.volume
        assert roof_solid > 0.999 and inner_solid > 0.999 and outer_solid > 0.999, (n, roof_solid, inner_solid, outer_solid)
        assert on_roof < 1e-3, f"pocket {n} undercuts a clip: {on_roof} mm3"
        pockets.append({"pawl": n, "radii_mm": [round(r0, 2), round(r1, 2)], "inner_radius_under_tip_mm": round(tip[0], 2),
                        "angles_deg_bose_frame": [round(tip[2], 2), round(a1, 2)],
                        "roof_solid_fraction": round(float(roof_solid), 4), "wall_0.6mm_inside_solid_fraction": round(float(inner_solid), 4),
                        "wall_0.6mm_outside_solid_fraction": round(float(outer_solid), 4),
                        "clip_material_standing_on_roof_mm3": round(float(on_roof), 3)})
    res["bose_pockets"] = pockets
    res["bose_material_removed_mm3"] = round(float(removed.volume), 2)

    # 4. glued: the arm, pushed flat, sweeps into the pocket and meets no Bose material
    if glued_bose is not None:
        slack = 0.3        # the arm's footprint grown by this, for a glue-up that is a little off
        for n, p in zip(names, pawls):
            step = p["narrow_from"] + slack * dl.DEG_PER_MM
            for r0, a0, a1 in ((dl.R_IN - slack, p["root"] - 0.5, step), (dl.R_TIP - slack, step, p["tip"] + slack * dl.DEG_PER_MM)):
                sweep = sector(r0, dl.R_OUT + slack, a0, a1, -(depth - 0.1), 0)
                assert common(sweep, glued_bose) is None, f"pawl {n} would hit the Bose half"
                turned = glued_bose.copy()         # the pins also allow the halves half a turn apart
                turned.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [0, 0, 1]))
                assert common(sweep, turned) is None, f"pawl {n} would hit the Bose half glued the other way round"
        res["arm_sweep_into_bose_half_overlap_mm3"] = 0.0
        res["arm_sweep_into_bose_half_turned_180_overlap_mm3"] = 0.0
    res["sweep"] = rows
    return res


if __name__ == "__main__":
    out = run()
    for r in out.pop("sweep"):
        print(r)
    import json
    print(json.dumps(out, indent=2))
