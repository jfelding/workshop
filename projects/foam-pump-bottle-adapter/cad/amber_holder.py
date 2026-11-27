"""Wall holder for the amber glass bottle with pump C (concept 7, hidden holder). Second version, from measurements.

Two printed parts:

- holder: one 30 mm wide profile. A spine glued to the wall behind the bottle (flat back, no holes), a foot bar under
  the glass that carries its weight, a low lip at the front of the foot, and a vertical dovetail
  channel at the top of the spine, open upwards.
- ring: a plain ring on the bare glass neck, just under the pump collar, with a dovetail key at the
  back. It goes on over the thread with the pump off; the screwed-on collar then keeps it on. The key
  drops into the channel, so the bottle cannot leave forward; it has to be lifted first.

The bottle's body, neck, thread and collar height are measured (measurements.py, 2026-11-24); the
shoulder's start and the pump head are still estimates, used only by the stand-in in amber_checks.py.

Both parts print on their side or upside down so that every load runs along the layers (see
log/decisions.md). Coordinates here are as installed: z = 0 is the foot top, where the glass
stands; +y points to the wall; the bottle axis is x = y = 0.

    uv run python cad/amber_holder.py     # writes exports/amber_holder.* and exports/amber_ring.*
"""
from pathlib import Path

from build123d import Axis, Plane, Polygon, Pos, extrude, offset, revolve

from workshop.cad.checks import fits_bed, overhangs
from workshop.cad.export import export
from workshop.cad.geometry import cylinder, prism_yz
from workshop.fits import hole_for, process
from workshop.measure import dims

import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
BED = (220, 220, 270)   # Neptune 3 Pro, equipment/neptune-3-pro/README.md

# --- derived layout ----------------------------------------------------------------------
W = dim("HOLDER_WIDTH")
gap = dim("HOLDER_BODY_GAP")
r_body_max = dim("AMBER_BODY_OD") / 2                   # measured body radius
y_spine = r_body_max + gap                             # spine front face
y_wall = y_spine + dim("HOLDER_SPINE_THICKNESS")
y_lip_in = -(r_body_max + gap)
y_lip_out = y_lip_in - dim("HOLDER_LIP_THICKNESS")
lip, lead = dim("HOLDER_LIP_HEIGHT"), dim("HOLDER_LIP_LEAD")
root, tip, g = dim("HOLDER_FOOT_ROOT"), dim("HOLDER_FOOT_TIP"), dim("HOLDER_GUSSET")
c = dim("HOLDER_CORNER_FILLET")

# ring on the bare neck under the collar: its bore must pass over the glass thread (44.0) to get there
ring_ri = hole_for(dim("AMBER_NECK_THREAD_OD"), "running") / 2
ring_ro = ring_ri + dim("RING_WALL")
ring_z1 = dim("AMBER_COLLAR_UNDERSIDE_Z") - dim("RING_UNDER_COLLAR")
ring_z0 = ring_z1 - dim("RING_THICKNESS")
# the neck under the collar: measured if anyone measures it, else Jacob's photo estimate (2026-11-26)
neck = m.AMBER_NECK_PROFILE or tuple((d + dim("EST_AMBER_NECK_PROFILE_DROP"), od) for d, od in m.EST_AMBER_NECK_PROFILE)
z_cu = dim("AMBER_COLLAR_UNDERSIDE_Z")


def bore_r(z):
    """Ring bore radius at height z: passes the glass thread (ring_ri) and, where the neck widens, follows it
    with the running fit's clearance, linear between the measured points."""
    if neck is None:
        return ring_ri
    up = dim("NECK_PROFILE_MARGIN_UP")
    pts = sorted((z_cu - d + up, hole_for(od, "running") / 2) for d, od in neck)   # (z, bore radius), bottom up
    assert pts[0][0] < ring_z0, "AMBER_NECK_PROFILE must reach below the ring's underside"
    for (za, ra), (zb, rb) in zip(pts, pts[1:]):
        if za <= z <= zb:
            return max(ring_ri, ra + (rb - ra) * (z - za) / (zb - za))
    return max(ring_ri, pts[-1][1] if z > pts[-1][0] else pts[0][1])


def bore_cutter():
    """The solid removed from the ring: straight, or a revolved profile following the measured neck."""
    if neck is None:
        return cylinder(ring_ri, 100, "z", (0, 0, ring_z0))
    up = dim("NECK_PROFILE_MARGIN_UP")
    zs = sorted({ring_z0 - 1, ring_z1 + 1, *(z_cu - d + up for d, _ in neck if ring_z0 - 1 < z_cu - d + up < ring_z1 + 1)})
    prof = [(0, zs[0])] + [(bore_r(z), z) for z in zs] + [(ring_ri, ring_z1 + 50), (0, ring_z1 + 50)]
    return revolve(Plane.XZ * Polygon(*prof, align=None), Axis.Z)


key_z0 = ring_z1 - dim("KEY_LENGTH")                   # key bottom = channel floor
z_top = ring_z1 + dim("SPINE_ABOVE_RING")
z_bot = -root - g

p = process()
slack = max(p.min_gap, p.printed_slide) / 2           # per side, key in channel (workshop.fits)
mouth, depth, flare = dim("KEY_MOUTH"), dim("KEY_DEPTH"), dim("KEY_FLARE")


def channel_outline(grow=0.0):
    """Dovetail section in the x-y plane, mouth at the spine face; `grow` < 0 gives the key."""
    hm, hb = mouth / 2, mouth / 2 + flare * depth
    pts = [(-hm, y_spine - 1), (hm, y_spine - 1), (hm, y_spine), (hb, y_spine + depth),
           (-hb, y_spine + depth), (-hm, y_spine)]
    poly = Polygon(*pts, align=None)
    return offset(poly, grow) if grow else poly


# --- holder: the side profile, extruded across x -----------------------------------------
profile = [(y_wall, z_bot), (y_wall, z_top), (y_spine, z_top), (y_spine, c), (y_spine - c, 0),
           (y_lip_in, 0), (y_lip_in, lip - lead), (y_lip_in - lead, lip), (y_lip_out, lip),
           (y_lip_out, -tip), (y_spine - g, -root)] + ([(y_spine, z_bot)] if g else [])
holder = prism_yz(profile, -W / 2, W / 2)
channel = extrude(Pos(0, 0, key_z0) * channel_outline(), z_top - key_z0 + 1)
holder -= channel

# --- ring with its key and the web behind it ---------------------------------------------
web_back = y_spine - dim("WEB_SPINE_GAP")             # web's back face, parallel to the spine's front face
web_hw = dim("WEB_BACK_HALF_WIDTH")
web_hr = dim("WEB_RING_HALF_WIDTH")                    # where the web's sides meet the ring's outside
web_yr = (ring_ro ** 2 - web_hr ** 2) ** 0.5
web_z0 = ring_z0                                       # flush with the ring underside: nothing hangs over the shoulder


def make_ring(key_grow, key_extra_length):
    """Ring + web + key. key_grow > 0 makes the key bigger than the channel, for filing to fit."""
    r = cylinder(ring_ro, ring_z1 - ring_z0, "z", (0, 0, (ring_z0 + ring_z1) / 2))
    kz0 = key_z0 - key_extra_length
    key = extrude(Pos(0, 0, kz0) * channel_outline(key_grow), ring_z1 - kz0)
    # web: a trapezoid in plan from the ring's back to just short of the spine face, as tall as the ring.
    # It fills the empty corner either side of the key, so a knock bends a wide plate instead of an 8 mm neck,
    # and its back face bears on the spine face when the ring is pushed towards the wall.
    web_pts = [(-web_hr, web_yr - 2), (web_hr, web_yr - 2), (web_hr, web_yr), (web_hw, web_back),
               (-web_hw, web_back), (-web_hr, web_yr)]
    web = extrude(Pos(0, 0, web_z0) * Polygon(*web_pts, align=None), ring_z1 - web_z0)
    r = r + key + web
    return r - bore_cutter()   # bore last


# as printed: key at KEY_OVERSIZE (play when negative) and a little long, its bottom filed if the ring sits high
ring = make_ring(dim("KEY_OVERSIZE"), dim("KEY_EXTRA_LENGTH"))
# as fitted: key filed to the printed sliding fit (workshop.fits) and to length; the fit checks use this
key_fit = -slack if dim("KEY_OVERSIZE") > 0 else dim("KEY_OVERSIZE")   # an oversize key is filed to the fits slide
ring_fitted = make_ring(key_fit, 0.0)
hk = mouth / 2 + key_fit

# --- print orientation --------------------------------------------------------------------
# holder on its side: the -x face on the bed, so spine and foot both lie in the layers.
holder_print = holder.rotate(Axis.Y, -90)
holder_print = holder_print.translate((0, 0, -holder_print.bounding_box().min.Z))
# ring upside down: its top face on the bed, the key standing up.
ring_print = ring.rotate(Axis.X, 180)
ring_print = ring_print.translate((0, 0, -ring_print.bounding_box().min.Z))

LAYOUT = dict(y_spine=y_spine, y_wall=y_wall, y_lip_in=y_lip_in, y_lip_out=y_lip_out, z_top=z_top,
              z_bot=z_bot, key_z0=key_z0, ring_ri=ring_ri, ring_ro=ring_ro, ring_z0=ring_z0, ring_z1=ring_z1,
              slack=slack, key_fit=key_fit, web_back=web_back, web_z0=web_z0)

if __name__ == "__main__":
    for name, part in (("amber_holder", holder_print), ("amber_ring", ring_print)):
        assert fits_bed(part, BED), name
        print(name, "overhangs", overhangs(part))
        export(name, part, OUT)
    if m.AMBER_NECK_PROFILE is None:
        print("NOTE: ring bore follows EST_AMBER_NECK_PROFILE, estimated from photos")
    print({k: round(v, 2) for k, v in LAYOUT.items()})
