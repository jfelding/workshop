"""Every physical dimension of door-phone-mute-switch-guard, in mm. The only place one is written down.

Each value says when and how it was measured. A value nobody has measured is None, and is
listed in ../inventory/to-measure.md with how to measure it. Parts read values through
workshop.measure.mm(), which refuses to build on None.

"Surface" below is the flat face of the handset that the toggle switch sticks out of.
"""

# --- measured -------------------------------------------------------------------------
# All by Jacob on the fitted switch, 2026-11-19, reported as "about".
BUSHING_THREAD_DIAMETER = 5.7    # outside of the threaded collar the nut sits on
NUT_ACROSS_FLATS = 9.0           # the hex nut, flat to flat
NUT_THICKNESS = 2.1              # the hex nut
THREAD_PAST_NUT = 1.5            # thread showing beyond the nut as fitted; 1.5-1.7 seen, the low end used

LEVER_TIP_HEIGHT = 15.0          # surface to the lever tip with the lever centred (its highest point), Jacob 2026-11-19
LEVER_SWING_SPAN = 10.4          # upper bound, not a reading: Jacob saw the tip stay inside the nut's outline at both
                                 # ends of the throw. The nut is 9.0 across flats = 10.4 across corners; the wider one used

# --- choices (not measurements; say why) ---------------------------------------------
FLOOR = 1.2          # 6 layers of 0.2 mm under the nut: fits in the 1.5 mm of spare thread
WALL = 1.6           # 4 perimeters at 0.4 mm: a jacket leaning on the rim does not flex it
RIM_ABOVE_LEVER = 3.0    # the lever tip sits this far below the rim, so cloth bulging in cannot reach it
RIM_CHAMFER = 0.8    # outer edge of the rim, so a sleeve slides over instead of catching
LEVER_CLEARANCE = 0.8    # per side around the lever's swing: the smallest gap that prints reliably
