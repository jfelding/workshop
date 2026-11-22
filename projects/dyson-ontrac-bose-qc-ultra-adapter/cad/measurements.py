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

# --- from a photo, NOT yet proven by fit (2026-11-22) ----------------------------------
# Read from the straight-on photo of the cushion back (PXL_20261117_153821423~2.jpg, 2899 x 2917 px)
# for the detent test variant only. The owner approved best guesses here and accepts a reprint.
# Method: ring centre fitted to the cushion plate's outer edge; scale 28.22 px/mm from
# SLOT_OPPOSING_SPAN (outer edges of the two long slots, 76.49 mm at a nominal 29 px/mm);
# cross-checks: slot chords read 33.3 (long, measured 33.5) and 22.0 (short, 22.4).
# Angles below are read in the PHOTO's own frame (counter-clockwise, 0 = right of the picture).
# The four slot centres in the photo are at 34.0, 114.5, 214.5 and 294.8 degrees, against
# SLOT_ANGLES -14, 68, 166, 248: the photo is turned +47.5 degrees from the SLOT_ANGLES frame
# with the SAME handedness (a mirrored reading leaves an 18-degree spread, this one 2), scatter
# +/-1 degree. Uncertainty: angles +/-1.5 degrees (about 1 mm), radii +/-0.3 mm.
PHOTO_FRAME_OFFSET_DEG = 47.5   # photo angle minus SLOT_ANGLES-frame angle
# One ledge bar per slot, in SLOT_ANGLES order: (kind, start, end, inner radius, outer radius).
# start = the end at the slot's closed end (the lock end), end = the end towards the open part.
# The outer radius is the slot's outer edge (SLOT_OPPOSING_SPAN / 2); the inner radius is where
# the pink slot floor ends under the bar (the short slot at 98-112 degrees is shaded: its
# inner face read 36.4-37.1, so 37.8 is used, the mean of the other three).
LEDGE_BARS_PHOTO = (
    ("long", 7.5, 22.8, 38.1, 39.3),
    ("short", 98.5, 112.3, 37.8, 39.3),
    ("long", 187.5, 203.2, 37.7, 39.3),
    ("short", 277.5, 293.6, 37.9, 39.3),
)
TWIST_TRAVEL_DEG = 16.0         # drop-on to home, "about 16 degrees" by hand (README); not measured
LEDGE_THICKNESS_ASSUMED = 0.8   # slab the lip clamps; ASSUMED equal to LIP_GAP_TRAILING (it clamps there)

# --- tuned / untested: detent bumps (first print will tell) -----------------------------
# Only the two LONG bars get a bump (a symmetric pair, so one part still serves both ears): the short
# slots sit where the plate is only 78 mm across, with no room for a bump under their bars.
BUMP_HEIGHT = 0.4               # 2 layers of 0.2. The bar clears the relief by only 0.2 (RELIEF_DEPTH -
                                # LEDGE_PROTRUSION), so 0.4 gives 0.2 mm of interference at full seating
BUMP_APPROACH_DEG = 20.0        # slope of the side the bar climbs first (towards drop-on): gentle
BUMP_RELEASE_DEG = 35.0         # slope on the home side: steeper, holds; a firm counter-twist still climbs it
BUMP_CREST_LENGTH = 1.0         # flat top along the arc, mm
BUMP_INNER_RADIUS = 38.2        # radial span of the bump: inside the bar's span (38.1 to 39.3 at the
BUMP_OUTER_RADIUS = 39.0        # worst bar) and clear of the seat edge (37.4) and the plate edge
CREST_BEFORE_HOME_DEG = 7.0     # how far from home the bar's trailing end is when it crosses the crest.
                                # Not smaller: the wedge lets the cushion lift only 0.2 mm at about 6 degrees from
                                # home and less closer (see detent_check.py), and the bump needs 0.2
