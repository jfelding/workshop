"""Every physical dimension of foam-pump-bottle-adapter, in mm. The only place one is written down.

Each value says when and how it was measured. A value nobody has measured is None, and is
listed in ../inventory/to-measure.md with how to measure it. Parts read values through
workshop.measure.mm(), which refuses to build on None.
"""

# --- measured (calipers, Jacob, 2026-11-19) ---------------------------------------------
BRACKET_HOLE_DIAMETER = 32.7             # black bracket (the one in the photos)
BRACKET_HOLE_DIAMETER_STAINLESS = 33.0   # second bracket, same kind, not pictured
NARROW_NECK_THREAD_OD = 27.5             # brown bottle, over the thread crests
NARROW_NECK_BORE = 21.3                  # brown bottle, inside the neck
WIDE_NECK_ROOT_OD = 39.0                 # clear square bottle, in the thread grooves
WIDE_NECK_THREAD_OD = 42.15              # clear square bottle, over the crests ("or so")
PUMP_A_STEM_MAX_OD = 31.45               # translucent-head pump (belongs to the clear bottle), widest below the collar
PUMP_B_STEM_MAX_OD = 21.1                # all-white pump, widest below the collar
PUMP_C_COLLAR_OD = 52.0                  # third pump (Jacob's favourite, no photo yet), outside of the collar
PUMP_C_BODY_OD = 32.0                    # third pump, body below the threads
PUMP_C_THREAD_ID = 43.85                 # inside pump C's collar at the threads; awkward to reach, "a bit more than" this. Treat as +-0.5
PUMP_C_COLLAR_WALL = 2.25                # thickness of the collar wall that carries the threads, approximate
PUMP_C_COLLAR_DEPTH = 14.6               # collar rim to inside ceiling, approximate
WIDE_NECK_BORE = 33.75                   # clear bottle, inside the neck
WIDE_NECK_HEIGHT = 21.25                 # clear bottle, neck top to shoulder
WIDE_NECK_THREAD_TURNS = 2               # count, not mm: two ridges at most above each other, one at some angles
BRACKET_PLATE_THICKNESS = 1.55           # black bracket
BRACKET_PLATE_THICKNESS_STAINLESS = 1.35
BRACKET_RING_OUTER_WIDTH = 50.0          # across the ring, both brackets, "about"
WIDE_NECK_THREAD_PITCH = 3.25            # clear bottle, "or so", not easy to measure; confirm with a printed test ring

# --- not yet measured (see ../inventory/to-measure.md) ------------------------------------
NARROW_NECK_ROOT_OD = None
NARROW_NECK_THREAD_PITCH = None
NARROW_NECK_HEIGHT = None
PUMP_B_THREAD_ID = None                  # inside the white pump's collar, crest to crest
PUMP_B_THREAD_ROOT_ID = None             # inside the white pump's collar, in the grooves
PUMP_B_THREAD_PITCH = None
PUMP_B_COLLAR_DEPTH = None               # how deep the collar is inside, rim to ceiling
PUMP_C_THREAD_ROOT_ID = None             # inside pump C's collar, in the grooves
PUMP_C_THREAD_PITCH = None
BRACKET_RING_FRONT_WIDTH = None          # metal between the hole and the ring's front edge; if equal to the sides (8.65) the front is a half circle around the hole

# --- choices (not measurements; say why) ---------------------------------------------------
GAUGE_STEP_DIAMETERS = (43.2, 43.6, 44.0, 44.4, 44.8, 45.2)   # brackets the rough 43.85 caliper reading of pump C's thread, 0.4 apart (about what the printer resolves)
GAUGE_STEP_HEIGHT = 3.0     # tall enough to put caliper jaws on a step afterwards
GAUGE_WALL = 2.4            # 6 perimeters at the narrowest step: stiff, and the bore stays wider than the pump's 32 mm body

# hanging collar (concept 6)
COLLAR_LENGTH = 12.0        # threaded length below the ring: over three turns of the 3.25 pitch, well short of the 21.25 neck
COLLAR_WALL = 2.4           # 6 perimeters outside the thread
COLLAR_WEB = 3.0            # wall at the front that rises past the ring's edge and carries the lips. Sets the outer circle: 57 mm against the pump's 52
COLLAR_RING_SIDE_PLAY = 0.5 # per side between ring edge and web: the ring width is only "about 50"
COLLAR_RING_LIFT = 0.6      # vertical play under the lips so the collar slides on; the bottle's neck takes it up when screwed tight
COLLAR_LIP_REACH = 3.0      # how far the lips reach in over the ring (ring metal is 8.65 wide); 45 degree underside prints without support
COLLAR_LIP_TIP = 1.0        # lip thickness at its inner edge
COLLAR_EDGE_CHAMFER = 0.8   # bottom outer edge: looks finished and hides the first layer's squish (elephant foot)
COLLAR_RAIL_MIN_WALL = 1.2  # the outside is one plain circle, so the web thins towards the back along the ring's straight sides; it stops where it would be thinner than this (3 perimeters)
THREAD_TIP_CLEARANCE = 0.6  # PROVISIONAL, radial, between the collar's thread tip and the neck's groove. Printed bottle threads are not in workshop.fits; the first print measures this
THREAD_TIP_WIDTH = 0.8      # PROVISIONAL, two extrusion widths
THREAD_BEARING_RUN = 0.3    # axial run of the upper (load-carrying) flank: nearly flat, so the bottle's weight does not wedge the collar open
THREAD_END_MARGIN = 1.5     # plain length at each end of the collar

# =========================================================================================
# ESTIMATED (not measured). Amber glass bottle with pump C, for the wall holder (concept 7).
# Jacob chose on 2026-11-22 to print from estimates and correct after a test print, overriding
# the measure-first rule for this part only. Every name starts with EST_ so no reader can take it
# for a caliper reading. Each says where it comes from and how far off it may be. Replace each
# with a measured name in the block above once measured (inventory/to-measure.md).
# =========================================================================================
EST_AMBER_BODY_OD = 65.0            # seller pages say 64-65; ±3 assumed. The holder is checked at 62 and 68
EST_AMBER_HEIGHT_NO_PUMP = 110.0    # seller pages, base to neck top; ±3 assumed
EST_AMBER_NECK_THREAD_OD = 43.0     # seller "43" fits the measured pump C thread ID 43.85 (a neck must be under it); 42-44
EST_AMBER_NECK_UNDER_COLLAR_OD = 40.0   # pure guess, 37-43. The holder does not touch the neck, so it does not matter to the fit
EST_AMBER_BODY_STRAIGHT = 82.0      # base to where the shoulder starts; guess from the seller photos' proportions, ±8
EST_AMBER_SHOULDER_TOP = 94.0       # where the shoulder meets the neck; guess, ±6
EST_AMBER_HEEL_RADIUS = 4.0         # rounded bottom edge of the glass; typical for moulded glass, 2-6
EST_PUMP_C_COLLAR_HEIGHT = 17.0     # outside height of pump C's collar: measured inside depth 14.6 plus a top wall; ±2
EST_PUMP_C_HEAD_TOP = 165.0         # base to top of the pump head, seller total height with pump; ±5
EST_PUMP_C_HEAD_OD = 40.0           # pump head width; looks narrower than the 52 collar in seller photos; 36-48
EST_PUMP_C_SPOUT_REACH = 45.0       # bottle axis to spout tip, horizontal; guess, 35-55
EST_PUMP_C_STROKE = 12.0            # how far the head goes down when pumped; typical foam pump, 8-15

# --- amber wall holder (concept 7): choices, not measurements ------------------------------
# z = 0 is the top of the foot, where the glass stands; +y points to the wall; the bottle axis is x = y = 0.
HOLDER_WIDTH = 30.0           # the whole holder is one 30 mm wide profile: narrower than the 65 bottle, so it hides behind it
HOLDER_BODY_GAP = 3.0         # radial air between the largest plausible body (EST + 3) and the spine / foot lip
HOLDER_SPINE_THICKNESS = 10.0 # wall plate; 5.5 mm behind the key channel. Kept stiff so it spreads the load evenly over the glue line instead of peeling at the top
HOLDER_FOOT_ROOT = 8.0        # foot bar thickness at the spine: carries the bending moment of the bottle and of pumping
HOLDER_FOOT_TIP = 5.0         # foot bar thickness at the front lip; thinner where the moment is small, and less to see
HOLDER_LIP_HEIGHT = 6.0       # front lip above the foot top. The bottle must rise this far before its base can move forward
HOLDER_LIP_THICKNESS = 3.0
HOLDER_LIP_LEAD = 2.0         # 45° chamfer on the lip's inner top edge, so the base finds its way in
HOLDER_GUSSET = 0.0           # 45° brace under the foot root, this tall and deep. 0: amber_strength.py shows the plain 8 mm root has SF 3.7 with the corner counted, so no brace
HOLDER_CORNER_FILLET = 2.0    # inside corner foot/spine (a 45° chamfer); the glass heel (EST 4 radius) clears it. Counted as Kt 1.5 in amber_strength.py
# wall fixing: none in the part. Jacob glues the spine's flat back to the wall with construction adhesive (montagelim), 2026-11-22
KEY_MOUTH = 8.0               # dovetail channel width at the spine's front face
KEY_DEPTH = 4.5               # how far the channel goes into the spine
KEY_FLARE = 1.2               # sideways growth per mm of depth: the channel's roof is 50° from flat when printed on its side
RING_COLLAR_PLAY = 1.5        # radial, ring bore to pump C's measured 52.0 collar: the ring never touches neck or collar threads
RING_WALL = 4.0              # radial. 3 gave a safety factor of 1.5 under the 20 N knock (amber_strength.py); 4 x 5 gives 3.2
RING_THICKNESS = 5.0
RING_REST_Z = 95.0            # ring underside when its key rests on the channel floor: the collar's estimated underside (110 - 14.6)
KEY_EXTRA_SLACK = 0.8         # normal to the flank, on the +x flank of the ring's key ONLY (the right side seen from above when the holder hangs on the wall). First print (Jacob's photos, 2026-11-22): the channel's roof flank (+x when printed on its side) came out ragged with sagged blobs. Instead of reprinting the holder, the key is slimmer on that flank. The -x flank stays at the fits slide play. Remove after a holder printed with a better channel
KEY_LENGTH = 16.0             # key hangs this far below the ring top; also the depth it sits in the channel
LINK_DROP = 3.0               # the ring-to-key link is this much deeper than the ring, for stiffness; still above the shoulder
SPINE_ABOVE_RING = 1.0        # spine top above the ring top: the spine stays below the collar's top and out of the spout's way

# --- amber holder: design loads and PLA allowables (Jacob, 2026-11-22), for amber_strength.py ---
LOAD_BOTTLE = 6.0             # N, full bottle, 0.6 kg
LOAD_PUSH = 30.0              # N, hard push down on the pump head, on the bottle axis
LOAD_KNOCK = 20.0             # N, sideways or forward knock on the bottle
PLA_ALONG_LAYERS = 45.0       # MPa, tensile, stress running along the layers
PLA_ACROSS_LAYERS = 25.0      # MPa, tensile, stress pulling layers apart
SAFETY_MIN = 3.0              # required safety factor against the allowable for the direction the stress runs
GLUE_ALLOWABLE = 0.5          # MPa, tension in the montagelim joint we allow ourselves: deliberately low, a fraction of the 1-2 MPa such adhesives are typically sold with; the real figure is on the tube
