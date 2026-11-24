"""Hand-calc strength check of the amber holder and ring: simple beams, numbers printed, SF asserted.

Loads (measurements.py): full bottle 6 N, a hard push down on the pump head 30 N on the bottle axis, a
20 N knock sideways or forward. PLA allowables depend on which way the stress runs relative to the layers:
45 MPa along, 25 MPa across. Each case names its direction for the print orientation in amber_holder.py
(holder on its side: layers are planes of constant x, so stress along y or z runs along the layers; ring
flat: layers are planes of constant z). Required: SF >= SAFETY_MIN against that allowable. Section sizes
are probed on the solid, not copied from the parameters. Writes exports/checks-amber-strength.json.

Deliberately conservative: the whole vertical load at the front edge of the base (bottle rocking forward
while pushed), the whole knock taken by the ring alone, the glue checked against a low allowable.

    uv run python cad/amber_strength.py
"""
import json
import math

from workshop.cad.checks import probe

import amber_holder as ah

dim, L = ah.dim, ah.LAYOUT
holder, ring = ah.holder, ah.ring
V = dim("LOAD_BOTTLE") + dim("LOAD_PUSH")          # N, down through the glass into the foot
K = dim("LOAD_KNOCK")
ALONG, ACROSS, SF = dim("PLA_ALONG_LAYERS"), dim("PLA_ACROSS_LAYERS"), dim("SAFETY_MIN")
W = dim("HOLDER_WIDTH")
x_front = -ah.r_body_max                           # base's front edge, largest plausible body
R = {}


def case(name, moment, z_mod, direction, note=""):
    """Bending stress M / Z against the allowable for `direction` ('along' or 'across' the layers)."""
    sigma = moment / z_mod
    allow = ALONG if direction == "along" else ACROSS
    sf = allow / sigma
    R[name] = dict(moment_Nmm=round(moment, 1), section_modulus_mm3=round(z_mod, 1), stress_MPa=round(sigma, 2),
                   layers=direction, allowable_MPa=allow, safety_factor=round(sf, 1),
                   safety_factor_vs_weak_25MPa=round(ACROSS / sigma, 1), note=note)
    print(f"{name:52s} σ = {sigma:5.2f} MPa ({direction} layers)  SF {sf:5.1f}  (vs 25 MPa: {ACROSS / sigma:4.1f})  {note}")
    assert sf >= SF, (name, sf)


def depth_at(y):
    """Vertical material of the foot at y, probed on the solid along x = 0."""
    return probe(holder, (0, y, 0.05), (0, y, -80)) if y < L["y_spine"] else None


# 1. foot as a cantilever off the spine; bending stress runs along y: along the layers (printed on its side)
KT_CORNER = 1.5   # 2 mm 45° inside corner on an 8 mm section, r/d = 0.25: shoulder-fillet charts give about 1.5
y_g = L["y_spine"] - dim("HOLDER_GUSSET")          # where a brace under the foot would end (none if 0)
d = depth_at(L["y_spine"] - dim("HOLDER_CORNER_FILLET") - 0.01)
case(f"1 foot root at the spine, d={d:.1f}, x Kt {KT_CORNER}", KT_CORNER * V * (L["y_spine"] - x_front), W * d ** 2 / 6,
     "along", f"{V:.0f} N at the base's front edge, arm {L['y_spine'] - x_front:.1f} mm")
lip_t = probe(holder, (0, L["y_lip_in"] + 0.05, 1.0), (0, -80, 1.0))
case(f"1 lip, base knocked forward, t={lip_t:.1f}", K * dim("HOLDER_LIP_HEIGHT"), W * lip_t ** 2 / 6, "along",
     f"{K:.0f} N at the lip top")

# 2. ring and key under the knock (taken by the ring alone)
w = probe(ring, (-ah.ring_ri + 0.05, 0, ah.ring_z0 + 1), (-80, 0, ah.ring_z0 + 1))
t = probe(ring, (-ah.ring_ri - w / 2, 0, ah.ring_z0 - 5), (-ah.ring_ri - w / 2, 0, 200))
r_mean = ah.ring_ri + w / 2
case(f"2 ring hoop, collar pushing, {w:.1f} x {t:.1f}", 0.318 * K * r_mean, t * w ** 2 / 6, "along",
     "thin ring, load and key reaction opposite: M = 0.318 F R")
hk = dim("KEY_MOUTH") / 2 - ah.slack
key_h = ah.ring_z1 - ah.key_z0                    # key's full height at the spine face; the web covers the rest
case(f"2 key neck at the spine face, sideways knock, {2 * hk:.1f} x {key_h:.1f}", K * L["y_spine"],
     key_h * (2 * hk) ** 2 / 6, "along", "knock at the bottle axis, arm to the spine face; the web stiffens everything in front")
key_d = dim("KEY_DEPTH") + 1 - 2 * ah.slack       # key's y depth, mouth to back
key_w = 2 * hk + dim("KEY_FLARE") * dim("KEY_DEPTH")   # mean width of the dovetail
case("2 key, forward knock, bends along its length", K * dim("KEY_LENGTH") / 2, key_w * key_d ** 2 / 6, "across",
     "key printed standing: its length is across the layers; reaction at mid-length")
flank_n = K / (2 * math.sin(math.atan(dim("KEY_FLARE"))))
case("2 channel lip, forward knock pulls the key", flank_n * dim("KEY_DEPTH") / 2,
     dim("KEY_LENGTH") * dim("KEY_DEPTH") ** 2 / 6, "across", f"{flank_n:.1f} N per flank; lip root is a layer plane")

# 3. glue joint and spine. The flat back (W x H) is glued to the wall: a rigid plate on a glue line, stress
#    linear over the height about its middle (M / (W H^2 / 6)) plus the downward load as shear (V / (W H)).
H = L["z_top"] - L["z_bot"]
spine_t = probe(holder, (0, L["y_spine"] - 0.05, 40), (0, 80, 40))
z_ring = (ah.ring_z0 + ah.ring_z1) / 2
z_mid = (L["z_top"] + L["z_bot"]) / 2
m_glue = V * (L["y_wall"] - x_front) + K * (z_ring - z_mid)   # bottle and push at the base's front edge, plus a forward knock at the ring
glue = dict(area_mm2=round(W * H, 0), moment_Nmm=round(m_glue, 0),
            peel_tension_MPa=round(m_glue / (W * H ** 2 / 6), 3), shear_MPa=round(V / (W * H), 3))
glue["safety_factor_vs_allowed"] = round(dim("GLUE_ALLOWABLE") / (glue["peel_tension_MPa"] + glue["shear_MPa"]), 1)
R["3 glue joint"] = glue
print(f"3 glue joint {W:.0f} x {H:.0f} mm: peak tension {glue['peel_tension_MPa']} MPa + shear {glue['shear_MPa']} MPa, "
      f"SF {glue['safety_factor_vs_allowed']} against the {dim('GLUE_ALLOWABLE')} MPa we allow the adhesive")
assert glue["safety_factor_vs_allowed"] >= SF
# The spine itself: worst section is just above the foot. Treat the glue as giving out over the lower
# third (pessimistic) so the spine has to carry the foot's moment up to there.
case(f"3 spine above the foot, {W:.0f} x {spine_t:.1f}", V * (L["y_spine"] - x_front), W * spine_t ** 2 / 6, "along",
     "full foot moment, as if the glue held nothing near the foot")
case("3 spine at the channel, forward knock at the ring", K * (z_ring - ah.key_z0), W * spine_t ** 2 / 6, "along",
     "channel top as a cantilever above the channel floor")

R["thicknesses_mm"] = dict(foot_at_lip=round(depth_at(L["y_lip_in"] + 0.5), 2), foot_at_root=round(d, 2), brace=dim("HOLDER_GUSSET"), lip=round(lip_t, 2),
                           spine=round(spine_t, 2), width=W, ring_wall=round(w, 2), ring_height=round(t, 2))
print("thicknesses:", R["thicknesses_mm"])
(ah.OUT / "checks-amber-strength.json").write_text(json.dumps(R, indent=1))
print("wrote", ah.OUT / "checks-amber-strength.json")
