"""Wall holder for the amber glass bottle with pump C (concept 7, hidden holder). ESTIMATED, untested.

Two printed parts:

- holder: one 30 mm wide profile. A spine glued to the wall behind the bottle (flat back, no holes), a foot bar under
  the glass that carries its weight, a low lip at the front of the foot, and a vertical dovetail
  channel at the top of the spine, open upwards.
- ring: a plain ring that goes over the pump collar and rests round its base, with a dovetail key
  at the back. The key drops into the channel. With the ring round the collar, the bottle cannot
  leave forward; it has to be lifted about 3 cm first, which is how it comes out.

The ring is loose on the bottle and sized from the one measured pump dimension (collar 52.0), so it
never touches the unknown glass neck. Every bottle dimension is an estimate (measurements.py,
ESTIMATED block); amber_checks.py checks the parts against a stand-in bottle over the plausible range.

Both parts print on their side or upside down so that every load runs along the layers (see
log/decisions.md). Coordinates here are as installed: z = 0 is the foot top, where the glass
stands; +y points to the wall; the bottle axis is x = y = 0.

    uv run python cad/amber_holder.py     # writes exports/amber_holder.* and exports/amber_ring.*
"""
from pathlib import Path

from build123d import Axis, Polygon, Pos, extrude, offset

from workshop.cad.checks import fits_bed, overhangs
from workshop.cad.export import export
from workshop.cad.geometry import box, cylinder, prism_yz
from workshop.fits import process
from workshop.measure import dims

import measurements as m

dim = dims(m)
OUT = Path(__file__).parents[1] / "exports"
BED = (220, 220, 270)   # Neptune 3 Pro, equipment/neptune-3-pro/README.md

# --- derived layout ----------------------------------------------------------------------
W = dim("HOLDER_WIDTH")
gap = dim("HOLDER_BODY_GAP")
r_body_max = (dim("EST_AMBER_BODY_OD") + 3) / 2        # the largest body the holder is built to take
y_spine = r_body_max + gap                             # spine front face
y_wall = y_spine + dim("HOLDER_SPINE_THICKNESS")
y_lip_in = -(r_body_max + gap)
y_lip_out = y_lip_in - dim("HOLDER_LIP_THICKNESS")
lip, lead = dim("HOLDER_LIP_HEIGHT"), dim("HOLDER_LIP_LEAD")
root, tip, g = dim("HOLDER_FOOT_ROOT"), dim("HOLDER_FOOT_TIP"), dim("HOLDER_GUSSET")
c = dim("HOLDER_CORNER_FILLET")

ring_ri = dim("PUMP_C_COLLAR_OD") / 2 + dim("RING_COLLAR_PLAY")
ring_ro = ring_ri + dim("RING_WALL")
ring_z0 = dim("RING_REST_Z")
ring_z1 = ring_z0 + dim("RING_THICKNESS")
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

# --- ring with its key --------------------------------------------------------------------
ring = cylinder(ring_ro, ring_z1 - ring_z0, "z", (0, 0, (ring_z0 + ring_z1) / 2))
key = extrude(Pos(0, 0, key_z0) * channel_outline(-slack), ring_z1 - key_z0)
hk = mouth / 2 - slack
link = box(-hk, hk, ring_ri + 1.0, y_spine, ring_z1 - dim("RING_THICKNESS") - dim("LINK_DROP"), ring_z1)
ring = ring + key + link
ring -= cylinder(ring_ri, 100, "z", (0, 0, ring_z0))   # bore last

# --- print orientation --------------------------------------------------------------------
# holder on its side: the -x face on the bed, so spine and foot both lie in the layers.
holder_print = holder.rotate(Axis.Y, -90)
holder_print = holder_print.translate((0, 0, -holder_print.bounding_box().min.Z))
# ring upside down: its top face on the bed, the key standing up.
ring_print = ring.rotate(Axis.X, 180)
ring_print = ring_print.translate((0, 0, -ring_print.bounding_box().min.Z))

LAYOUT = dict(y_spine=y_spine, y_wall=y_wall, y_lip_in=y_lip_in, y_lip_out=y_lip_out, z_top=z_top,
              z_bot=z_bot, key_z0=key_z0, ring_ri=ring_ri, ring_ro=ring_ro, ring_z0=ring_z0, ring_z1=ring_z1,
              slack=slack)

if __name__ == "__main__":
    for name, part in (("amber_holder", holder_print), ("amber_ring", ring_print)):
        assert fits_bed(part, BED), name
        print(name, "overhangs", overhangs(part))
        export(name, part, OUT)
    print({k: round(v, 2) for k, v in LAYOUT.items()})
