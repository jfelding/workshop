"""Every physical dimension of __NAME__, in mm. The only place one is written down.

Each value says when and how it was measured. A value nobody has measured is None, and is
listed in ../inventory/to-measure.md with how to measure it. Parts read values through
workshop.measure.mm(), which refuses to build on None.
"""

# --- measured -------------------------------------------------------------------------
SHAFT_DIAMETER = 6.0        # stainless pin, calipers, __DATE__
NUT_M3_ACROSS_FLATS = 5.5   # calipers
NUT_M3_THICKNESS = 2.4      # calipers

# --- not yet measured ------------------------------------------------------------------
MOUNT_HOLE_SPACING = None   # see ../inventory/to-measure.md

# --- choices (not measurements; say why) ---------------------------------------------
WALL = 3.0                  # 7–8 perimeters at 0.4 mm: stiff enough for a hand-tightened bolt
