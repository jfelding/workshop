"""Every physical dimension of the Dyson OnTrac -> Bose QuietComfort Ultra cushion adapter, in mm.

The only place a dimension is written down. Parts read values through workshop.measure.mm().
Three kinds of number live here, and each says which it is:

- measured: calipers on the Dyson cushion (2026-11-16), or read off the Bose frame mesh;
- from a photo: the slot angles. They could not be measured with calipers, so they were read
  from a straight-on photo and then proven by the printed part fitting;
- tuned: found by test prints (twelve of them). These are what you change to adjust the fit.
"""

# --- measured: Dyson OnTrac cushion, calipers, 2026-11-16 ------------------------------
# The back of the cushion has four curved slots on a circle (two long, two short). Each slot
# is wide for most of its length and has a ledge closing over one end, which is what a hook
# turns under.
SLOT_OPPOSING_SPAN = 78.6      # across two opposite slots, outer edge to outer edge
SLOT_LONG_CHORD = 33.5         # straight end-to-end length of a long slot (33.3-33.7)
SLOT_SHORT_CHORD = 22.4        # ...of a short slot (22.3-22.5)
SLOT_WIDE_WIDTH = 5.3          # radial width of the open part of a slot
SLOT_NARROW_WIDTH = 3.9        # radial width under the ledge
SLOT_DEPTH = 3.3               # face of the cushion plate to the slot floor
LEDGE_PROTRUSION = 0.6         # the ledge blocks stand this far proud of the cushion face
CUSHION_OPENING_DIAMETER = 60.5   # round sound opening in the cushion's back plate

# --- measured: Bose earpad frame, read from vendor/bose-earpad-frame/frame_body1.stl ----
BOSE_OVAL_X = 78.0             # outline of the frame, an ellipse within 0.08 mm: short axis
BOSE_OVAL_Y = 96.5             # ...long axis
BOSE_OPENING_X = 60.0          # inner opening of the frame, also an ellipse
BOSE_OPENING_Y = 78.5
BOSE_FRAME_THICKNESS = 2.0     # the flat plate the pins go into (the clips stand taller)

# --- from a photo, proven by fit -------------------------------------------------------
# (centre angle in degrees, kind) of each slot, looking at the back of the cushion.
SLOT_ANGLES = ((-14.0, "long"), (68.0, "short"), (166.0, "long"), (248.0, "short"))
# Rotation of the hook pattern on the plate, so that the cushion's oval ear opening ends up
# along the long axis of the Bose oval once the cushion is twisted home.
CUSHION_CLOCKING_DEG = 76.0

# --- tuned by test prints (PLA, 0.4 mm nozzle, 0.2 mm layers) --------------------------
PLATE_THICKNESS = 2.0          # at the seat; the plate is thinner outside it (RELIEF_DEPTH)
RELIEF_DEPTH = 0.8             # step down outside the seat: the proud ledge blocks pass over it
BORE_DIAMETER = 61.6           # sound opening through the plate
STEM_OUTER_RADIUS = 37.4       # outer face of every hook stem, and the edge of the raised seat
STEM_INNER_RADIUS = {"short": 34.4, "long": 36.0}   # long slots are narrower in practice: 1.4 mm stem
LIP_OUTER_RADIUS = {"short": 38.9, "long": 38.9}    # how far the lip reaches under the ledge
LIP_FLAT_FROM_RADIUS = 37.9    # the lip's underside is flat outward of this: the face that holds
LIP_UNDERSIDE_SLOPE_DEG = 45.0  # inward of it the underside slopes, so it prints without support
LIP_GAP_LEADING = 1.4          # gap between seat and lip at the end that enters under the ledge first
LIP_GAP_TRAILING = 0.8         # ...at the other end: the wedge that pulls the cushion down and clamps
LIP_END_RAMP = 1.3             # plan-view 45-degree lead-in on both ends of each lip
HOOK_HEIGHT = 2.7              # top of the hook above the seat (the slot is 3.3 deep)
HOOK_TIP_CHAMFER = 0.8         # inner top edge
HOOK_LENGTH = 9.0              # along the slot, measured at the middle of the stem
LOCK_END_GAP = 1.5             # hook stops this far short of the slot's closed end when locked
FRONT_EDGE_FILLET = 0.6        # cushion side, outer oval
BORE_EDGE_FILLET = 0.4         # cushion side, bore
BACK_EDGE_CHAMFER = 0.3        # glue side: absorbs elephant foot and leaves a crisp seam

# --- alignment pins: two offcuts of 1.75 mm filament ------------------------------------
PIN_ANGLES_DEG = (80.0, 260.0)  # on the glue band, clear of the hooks, the Bose clips and its text
PIN_SLIP_HOLE = 1.95           # through the Dyson half; small printed holes come out 0.1-0.2 under
PIN_PRESS_POCKET = 1.85        # blind, in the Bose half
PIN_POCKET_DEPTH = 1.4         # of the 2.0 mm Bose plate, so the earcup side stays closed
PIN_HOLE_CHAMFER = 0.3
