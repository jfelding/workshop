"""Checks the amber holder and ring against a STAND-IN bottle and pump, over the plausible range.

The stand-in is built from the measured bottle (2026-11-24); where its body stops being straight, its heel
and the pump head are still estimates.
It is a check shape, not a model of the real bottle. Each check prints a number and fails the build
when a clearance is broken. Writes exports/checks-amber.json.

    uv run python cad/amber_checks.py
"""
import json
import math

import numpy as np
from build123d import Axis, Plane, Polygon, revolve

from workshop.cad.checks import overlap, overhangs, probe
from workshop.cad.geometry import box, cylinder
from workshop.cad.printability import layers, mesh_check

import amber_holder as ah

dim, L = ah.dim, ah.LAYOUT
OUT = ah.OUT


def stand_in(body_od=None, shoulder_start=None, neck_up=0.0):
    """(glass, pump) solids, installed pose: glass base on z = 0, axis on z. Spout points to -y (front)."""
    body_od = body_od or dim("AMBER_BODY_OD")
    z_cu = dim("AMBER_COLLAR_UNDERSIDE_Z")
    h = z_cu + dim("PUMP_C_COLLAR_DEPTH")              # neck top against the collar's inside ceiling
    rb, rn = body_od / 2, dim("AMBER_NECK_UNDER_COLLAR_OD") / 2
    rt, hr = dim("AMBER_NECK_THREAD_OD") / 2, dim("EST_AMBER_HEEL_RADIUS")
    z_sh1 = z_cu - dim("AMBER_NECK_BARE_HEIGHT")       # measured: where the neck starts widening
    z_sh0 = shoulder_start if shoulder_start is not None else dim("EST_AMBER_BODY_STRAIGHT")   # estimated: where the body stops being straight
    heel = [(rb - hr + hr * math.sin(a), hr - hr * math.cos(a)) for a in np.linspace(0, math.pi / 2, 7)]
    if ah.neck is None:   # a straight cone from the body to the neck
        neck = [(rb, z_sh0), (rn, z_sh1), (rn, z_cu)]
    else:                 # the measured neck, then straight down to the body below its deepest point
        pts = sorted((z_cu - d + neck_up, od / 2) for d, od in ah.neck)
        neck = [(rb, min(z_sh0, pts[0][0] - 0.2)), *[(r, z) for z, r in pts if z <= z_cu]]
        if neck[-1][1] < z_cu:
            neck.append((neck[-1][0], z_cu))
    prof = [(0, 0), *heel, *neck, (rt, z_cu), (rt, h), (0, h)]
    glass = revolve(Plane.XZ * Polygon(*prof, align=None), Axis.Z)
    z_ct = z_cu + dim("EST_PUMP_C_COLLAR_HEIGHT")
    head_top = dim("EST_PUMP_C_HEAD_TOP")
    head_h = 25.0   # stand-in shape only
    collar = cylinder(dim("PUMP_C_COLLAR_BASE_OD") / 2, z_ct - z_cu, "z", (0, 0, (z_cu + z_ct) / 2))
    stem = cylinder(8, head_top - head_h - z_ct, "z", (0, 0, (z_ct + head_top - head_h) / 2))
    head = cylinder(dim("EST_PUMP_C_HEAD_OD") / 2, head_h, "z", (0, 0, head_top - head_h / 2))
    spout = box(-5, 5, -dim("EST_PUMP_C_SPOUT_REACH"), 0, head_top - 14, head_top - 4)
    return glass, collar + stem, head + spout, dict(z_cu=z_cu, z_ct=z_ct, z_sh0=z_sh0, z_sh1=z_sh1, rb=rb, rn=rn)


def ring_seat(info):
    """Where the ring sits: on the channel floor, or lifted by the shoulder if that is higher."""
    if ah.neck is not None:   # the bore follows the measured neck: it seats on the key, not on the glass
        return 0.0, ah.ring_z0
    rb_sh = ah.ring_ri   # shoulder radius where it meets the ring bore
    rb, rn, z_sh0, z_sh1 = info["rb"], info["rn"], info["z_sh0"], info["z_sh1"]
    z_touch = z_sh0 + (rb - rb_sh) / (rb - rn) * (z_sh1 - z_sh0)
    return max(0.0, z_touch - ah.ring_z0), z_touch


def first_contact(moving, fixed, direction, limit=60, step=0.25):
    """Distance the moving solid travels along `direction` before it meets `fixed`."""
    d = 0.0
    while d <= limit:
        if overlap(moving.translate(tuple(d * k for k in direction)), fixed) > 0:
            return d
        d += step
    return None


R = {}
holder, ring = ah.holder, ah.ring_fitted   # the key as filed to fit; the printed one is oversized
glass, pump_low, pump_head, info = stand_in()
lift, z_touch = ring_seat(info)
ring_in = ring.translate((0, 0, lift))
R["stand_in"] = {k: round(v, 2) for k, v in info.items()}
R["ring_rest_z"] = ah.ring_z0
R["printed_key_material_to_file_mm3"] = round(overlap(ah.ring.translate((0, 0, dim("KEY_EXTRA_LENGTH"))), holder), 1)
R["web_back_to_spine_face_mm"] = round(L["y_spine"] - L["web_back"], 2)
R["shoulder_meets_ring_bore_z"] = round(z_touch, 2)

# 1. installed pose: nothing overlaps
pairs = {"holder/glass": (holder, glass), "holder/pump": (holder, pump_low + pump_head),
         "ring/glass": (ring_in, glass), "ring/pump": (ring_in, pump_low + pump_head),
         "ring/holder": (ring_in, holder)}
R["installed_overlap_mm3"] = {k: round(overlap(a, b), 3) for k, (a, b) in pairs.items()}
assert all(v == 0 for v in R["installed_overlap_mm3"].values()), R["installed_overlap_mm3"]

# clearances in the installed pose (mm)
bottle = glass + pump_low
R["clearance_mm"] = {
    "body to spine": round(L["y_spine"] - dim("AMBER_BODY_OD") / 2, 2),
    "body to foot lip": round(-L["y_lip_in"] - dim("AMBER_BODY_OD") / 2, 2),
    "neck to ring bore, radial": round(ah.ring_ri - dim("AMBER_NECK_UNDER_COLLAR_OD") / 2, 2),
    "thread to ring bore, radial (getting it on)": round(ah.ring_ri - dim("AMBER_NECK_THREAD_OD") / 2, 2),
    "ring top below collar": round(info["z_cu"] - ah.ring_z1, 2),
    "ring outside minus collar outside, radial": round(ah.ring_ro - dim("PUMP_C_COLLAR_BASE_OD") / 2, 2),
    "spine top below collar top": round(info["z_ct"] - L["z_top"], 2),
}

# 2. the bottle cannot leave forward while the ring is in the channel
R["forward_travel_until_ring_stops_bottle_mm"] = first_contact(bottle, ring_in, (0, -1, 0))
R["forward_travel_until_lip_stops_base_mm"] = first_contact(glass, holder, (0, -1, 0))
R["ring_forward_travel_in_channel_mm"] = first_contact(ring_in, holder, (0, -1, 0))
R["upward_travel_until_shoulder_lifts_ring_mm"] = first_contact(glass, ring_in, (0, 0, 1), limit=40)
assert R["forward_travel_until_ring_stops_bottle_mm"] is not None and R["forward_travel_until_ring_stops_bottle_mm"] < 2
assert R["forward_travel_until_lip_stops_base_mm"] is not None and R["forward_travel_until_lip_stops_base_mm"] < 3

# 3. insertion / removal path: lift until the key is clear of the spine, then forward
key_rise = L["z_top"] - L["key_z0"] + 2.0          # key bottom 2 mm above the spine top
lift_total = lift + (R["upward_travel_until_shoulder_lifts_ring_mm"] or 0) + key_rise
R["lift_to_remove_mm"] = round(lift_total, 1)
hit = []
for dz in np.arange(0, lift_total + 0.01, 1.0):     # straight up: horizontal gaps, so 1 mm steps miss nothing
    if overlap(bottle.translate((0, 0, dz)), holder) > 0:
        hit.append(("up", float(dz)))
ring_up = ring_in.translate((0, 0, key_rise))
for dy in np.arange(0, 90.01, 2.0):                 # then forward over the lip and away from the spine
    mv = (0, -dy, lift_total)
    if overlap(bottle.translate(mv), holder) > 0 or overlap(ring_up.translate((0, -dy, 0)), holder) > 0:
        hit.append(("forward", float(dy)))
R["insertion_path_contacts"] = hit
assert not hit, hit
R["base_above_lip_when_lifted_mm"] = round(lift_total - dim("HOLDER_LIP_HEIGHT"), 1)

# 4. pump head and spout, at rest and pushed down, spout turned to front, side and wall
spout_hits = {}
for turn in (0, 90, 180):
    for push in (0, dim("EST_PUMP_C_STROKE")):
        hd = pump_head.rotate(Axis.Z, turn).translate((0, 0, -push))
        spout_hits[f"turn {turn}°, pushed {push:g}"] = round(overlap(hd, holder) + overlap(hd, ring_in), 3)
R["pump_head_overlap_mm3"] = spout_hits
assert all(v == 0 for v in spout_hits.values()), spout_hits
R["pump_head_bottom_above_spine_top_pushed_mm"] = round(
    dim("EST_PUMP_C_HEAD_TOP") - 25 - dim("EST_PUMP_C_STROKE") - L["z_top"], 1)

# 5. the plausible range: body ±0.5 mm (moulded glass), the estimated shoulder start ±5 mm
rng = {}
for od in (dim("AMBER_BODY_OD") - 0.5, dim("AMBER_BODY_OD"), dim("AMBER_BODY_OD") + 0.5):
    for hh in (dim("EST_AMBER_BODY_STRAIGHT") - 5, dim("EST_AMBER_BODY_STRAIGHT") + 5):
        g2, pl2, ph2, i2 = stand_in(od, hh)
        lf, zt = ring_seat(i2)
        r2 = ring.translate((0, 0, lf))
        ov = overlap(holder, g2 + pl2 + ph2) + overlap(r2, g2 + pl2)
        holds = zt <= ah.ring_z0 + lf + 0.01 and ah.ring_z0 + lf < i2["z_ct"]
        rng[f"body {od:g}, shoulder starts {hh:g}"] = dict(overlap_mm3=round(ov, 3), ring_lifted_mm=round(lf, 2),
                                                 ring_round_collar_or_neck=holds)
        assert ov == 0 and holds, (od, hh, ov, holds)
# the neck estimate's error, now calibrated by the v4 fit: every point up to the bore's margin (clashes first) and 1 down (rattles)
for nu in (dim("NECK_PROFILE_MARGIN_UP"), -1.0):
    g3, pl3, _, _ = stand_in(neck_up=nu)
    ov3 = overlap(ring, g3 + pl3)
    up3 = first_contact(g3, ring, (0, 0, 1), limit=20, step=0.1)
    rng[f"neck profile {nu:+g} mm"] = dict(overlap_mm3=round(ov3, 3), glass_rise_until_it_lifts_ring_mm=up3)
    assert ov3 == 0, (nu, ov3)
R["plausible_range"] = rng

# nothing of the ring hangs below its underside inside the body outline (only the key, which is outside the glass)
below = ring.intersect(cylinder(dim("AMBER_BODY_OD") / 2, ah.ring_z0 - 40, "z", (0, 0, (ah.ring_z0 + 40) / 2)))
R["ring_volume_below_underside_inside_body_outline_mm3"] = round(below.volume if below else 0.0, 3)
assert R["ring_volume_below_underside_inside_body_outline_mm3"] == 0, R["ring_volume_below_underside_inside_body_outline_mm3"]
R["ring_bore_follows_neck"] = ah.neck is not None
R["ring_wall_at_underside_mm"] = round(ah.ring_ro - ah.bore_r(ah.ring_z0), 2)
assert R["ring_wall_at_underside_mm"] >= 1.6, R["ring_wall_at_underside_mm"]   # 4 perimeters
R["bare_neck_the_ring_needs_mm"] = round(dim("RING_UNDER_COLLAR") + dim("RING_THICKNESS"), 2)

# 6. walls, from the solid
y_s, y_w = L["y_spine"], L["y_wall"]
R["walls_mm"] = {
    "spine behind the key channel": round(probe(holder, (0, y_s + 0.05, 90), (0, 60, 90)), 2),
    "spine at mid height": round(probe(holder, (0, y_s - 0.05, 40), (0, 60, 40)), 2),
    "foot at the spine (vertical)": round(probe(holder, (0, y_s - 3, 2), (0, y_s - 3, -60)), 2),
    "foot at the lip (vertical)": round(probe(holder, (0, L["y_lip_in"] + 0.5, -0.05), (0, L["y_lip_in"] + 0.5, -60)), 2),
    "channel side wall": round(probe(holder, (dim("KEY_MOUTH") / 2 + dim("KEY_FLARE") * dim("KEY_DEPTH") + 0.05, y_s + dim("KEY_DEPTH") - 0.2, 90), (40, y_s + dim("KEY_DEPTH") - 0.2, 90)), 2),
    "ring wall": round(probe(ring, (-ah.ring_ri + 0.05, 0, ah.ring_z0 + 2), (-60, 0, ah.ring_z0 + 2)), 2),
}

# 7. printability, on the solids in print orientation and on the exported meshes
for name, part in (("amber_holder", ah.holder_print), ("amber_ring", ah.ring_print)):
    o = overhangs(part)
    verts, tris = part.tessellate(0.05, 0.2)
    V = np.array([[v.X, v.Y, v.Z] for v in verts]); T = np.array(tris)
    n = np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]])
    nz = n[:, 2] / np.maximum(np.linalg.norm(n, axis=1), 1e-12)
    up = V[T].mean(axis=1)[:, 2] > 0.05
    worst = float(np.degrees(np.arcsin(np.clip(-nz[up].min(), 0, 1)))) if up.any() else 0.0
    b = part.bounding_box().size
    stl = OUT / f"{name}.stl"
    mc = mesh_check(stl)
    summ, _ = layers(stl)
    R[name] = dict(size_mm=[round(b.X, 1), round(b.Y, 1), round(b.Z, 1)], volume_cm3=round(part.volume / 1000, 1),
                   overhang_steeper_than_45_mm2=round(o["steeper_than_45_mm2"], 1),
                   flat_ceilings_mm2=round(o["flat_ceilings_mm2"], 1),
                   worst_overhang_deg_from_vertical=round(worst, 1),
                   mesh=mc, layers_outside_45_mm2=summ["max_area_outside_45deg_layer_envelope_mm2"],
                   islands_in_mid_air=len(summ["new_islands_without_previous_layer_overlap"]))

for k, v in R.items():
    print(f"{k}: {v}")
(OUT / "checks-amber.json").write_text(json.dumps(R, indent=1, default=str))
print("wrote", OUT / "checks-amber.json")
