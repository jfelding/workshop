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
