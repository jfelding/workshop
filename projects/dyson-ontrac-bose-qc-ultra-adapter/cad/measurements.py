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
BUMP_INNER_RADIUS = 38.1        # radial span of the bump: inside the bar's span (38.1 to 39.3 at the
BUMP_OUTER_RADIUS = 39.3        # worst bar) and clear of the seat edge (37.4) and the plate edge
CREST_BEFORE_HOME_DEG = 7.0     # how far from home the bar's trailing end is when it crosses the crest.
                                # Not smaller: the wedge lets the cushion lift only 0.2 mm at about 6 degrees from
                                # home and less closer (see detent_check.py), and the bump needs 0.2

# --- from a photo, NOT yet proven by fit (2026-11-22): the cushion's hard back ring ---------
# Outer edge of the hard black ring, where it meets the pink foam, read from the same photo and scale
# (28.22 px/mm) at 72 angles. The ring is a circle: fitted centre within 3 px (0.1 mm) of the slot circle's,
# radius 41.13 mm, scatter 0.12 mm (41.0 to 41.4 at 0, 30, ..., 330 degrees). Uncertainty +/-0.4 mm
# (scale 1 percent). Calipers: across the ring at the widest, outside jaws, then halve.
RING_OUTER_RADIUS = 41.1

# --- tuned / untested: wide outline (dyson_half_wide) ----------------------------------
# The plate outline is the Bose oval united with a circle, blended: it bulges out around the short axis
# so the plate covers the hard ring (the oval is only 39.0 mm from the centre there).
COVER_MARGIN = 0.4              # beyond the ring: the top edge is rounded 0.6, so the flat face ends about
                                # 0.2 mm inside the ring edge; and the ring reading is +/-0.4 mm
COVER_RADIUS = RING_OUTER_RADIUS + COVER_MARGIN
OUTLINE_BLEND_RADIUS = 40.0     # fillet where the circle meets the oval, mm: large, so no corner shows

# --- tuned / untested: spring latch (dyson_half_latch + bose_half_latch, 2026-11-23) -----------------
# The printed detent bumps gave no click (0.2 mm of interference between rigid parts, no spring). The
# latch is a pawl instead: a flexure arm (a strip cut free from the plate on three sides, so it bends
# like a leaf spring) with a tooth on its free end. One pawl per SHORT slot. The cushion's solid face
# holds the tooth down from drop-on; at home the slot's open-end wall has moved past the tooth, which
# springs up into the slot behind that wall. Twisting back, the wall meets the tooth's sloped face and
# has to push the pawl down again. Angles are in the plate (CAD) frame, like the hooks.
LATCH_ARM_INNER_RADIUS = 34.8   # arm and tooth, radially. The short slot spans 34.0 to 39.3 (calipers:
LATCH_ARM_OUTER_RADIUS = 37.4   # SLOT_OPPOSING_SPAN, SLOT_WIDE_WIDTH); the proven hook stem is 34.4-37.4.
                                # Outer = seat edge, so the arm stays inside the seat, clear of the bars
LATCH_TOOTH_INNER_RADIUS = 35.3 # the arm's tip and the tooth are narrower on the inside: the Bose frame has a
                                # clip there (out to radius 34.65, from the vendor mesh), and the pocket under
                                # the arm must not undercut it
LATCH_NARROW_BEFORE_FOOT = 2.2  # the narrow tip starts this far (mm) before the tooth's lock face
LATCH_SLIT_WIDTH = 0.8          # gap cut round the arm, two nozzle widths so it does not fuse shut
LATCH_ARM_TOP_BELOW_SEAT = 0.2  # arm top is lower than the seat, so only the tooth touches the cushion;
                                # arm thickness = PLATE_THICKNESS - this = 1.8
LATCH_TOOTH_HEIGHT = 1.2        # tooth above the seat (the slot is 3.3 deep). Also the arm's deflection
LATCH_LOCK_FACE_DEG = 65.0      # slope of the face the slot wall pushes on, from flat. Steeper holds
                                # harder. Keep under 70: a vertical face could only be released by breaking it
LATCH_BACK_FACE_DEG = 75.0      # the other face, never loaded. Steep, to keep the arm's tip short: the
                                # Bose frame has a clip just past it, which the pocket must not undercut
LATCH_TOOTH_CREST = 0.8         # flat top along the arc, mm (two wall lines)
LATCH_FOOT_BEHIND_WALL_DEG = (-2.8, -2.8)  # where each tooth's lock face starts, behind (+) or ahead of (-)
                                # the slot wall's nominal home position. First print (2026-11-23, values -0.7 and
                                # 0.9): only the earlier tooth came up, and only when twisted hard, so the cushion
                                # stops 1 to 2 degrees BEFORE nominal home. Both teeth are now fully up 3.0 degrees
                                # before nominal home. More negative = up earlier = more play
LATCH_ARM_LENGTH_DEG = 23.0     # lock-face foot to the arm's root, along the arc (about 14.5 mm)
LATCH_LOWER_PAST_ROOT = 1.5     # the lowered top runs this far (mm) past the root, so the 0.2 step is
                                # not at the most stressed spot
BOSE_LATCH_POCKET_DEPTH = 1.6   # relief pocket in the Bose half under each arm (plate 2.0, so 0.4 stays)
BOSE_LATCH_POCKET_MARGIN = 0.4  # pocket is this much larger radially than arm plus slits (glue stays off)
BOSE_LATCH_POCKET_END_MARGIN = 0.4   # and this much longer at each end
BOSE_LATCH_POCKET_TIP_CLEARANCE = 0.55   # under the narrow tip the pocket's inner wall is this far inside the
                                # arm (radius 34.75, just outside the clip), and its step is this far past the arm's
                                # own step, so a glue-up that is 0.3 mm off still leaves the arm free
PLA_MODULUS_ASSUMED_MPA = 2500  # textbook stiffness of printed PLA (2300-3500), NOT measured here. Only
                                # used to report the spring force; no dimension depends on it
