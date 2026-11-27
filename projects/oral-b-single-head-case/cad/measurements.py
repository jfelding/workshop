"""Every dimension of oral-b-single-head-case, in mm. The only place one is written down.

The part is DrJones's two-head case (vendor/oralbox2/) cut down to one head. Every position below was read from the
vertices and a 0.5 mm height map of vendor/oralbox2/oralbox2.stl on 2026-11-27. Nothing is measured on a brush head:
the single case gives the head exactly the room the original does, wherever the head can be.

Coordinates are the original file's: the case lies open, hinge axis along X at y = 0, the cradle half (the one
with the clips that hold the heads) at y < 0, the stand half (two pegs, vents, latch tab) at y > 0.

How a head lies (DrJones's photo, and the clip): the neck sits in the clip with its axis at y = -10, z = 9.5, which
is the plane the case closes on. The two heads lie head to tail and their bristles point sideways, toward the outer
wall, into the room beside the other head's tube end. So:
- at the bristle end (from the end wall to the clip) the head may use the full original width;
- past the clip only the tube is left, and it fits one 15 mm lane, as the original's second tube lies beside it.
"""

# --- read from the original mesh ----------------------------------------------------------
LANE_PITCH = 15.0               # clips centred at y = -10.0 and -25.0
CRADLE_A_Y = (-15.548, -4.452)  # the clip kept, near the hinge
CRADLE_A_X = (18.0, 26.5)       # it grips the neck just behind the bristle head, so the bristles are at x < 18
CRADLE_B_BOX = ((73.5, 82.0), (-30.548, -19.452))      # the far clip, removed: x range, y range
PEG_BOX = ((31.0, 69.0), (12.5, 22.0))                 # both stand pegs, cone feet included: x range, y range
FLOOR_TOP_Z = 1.5               # top of both floors
INNER_WALL_Y = 32.75            # inner face of each half's outer wall, |y| (fillet foot at 32.0)
LENGTH = 100.0                  # end wall outer face to end wall outer face
END_WALL_SLAB = 4.0             # end wall 2.0 thick, 1.0 fillet, 1.0 of plain floor: the slab copied as the step wall
END_CORNER_X = 3.0              # where the end wall's rounded outer corner starts, from the outer face

# --- choices (not measurements; say why) ---------------------------------------------------
STEP_WALL_X = 28.0              # outer face of the step wall. Its inner face is at 26.0, level with the end of the
                                # clip: the pocket for the bristles runs 8 mm past where the bristle head can be (18)
STAND_CUT_Y = (10.0, 25.0)      # the stand half's strip: centred on its floor and vents, clear of its walls
OVERLAP = 0.5                   # pieces joined in a plain floor-and-wall section overlap this far, so the union never
                                # meets coplanar faces
HINGE_TEST_LENGTH = 20.0        # end wall and three whole knuckles (cradle 5-10, stand 10-15, cradle 15-20 mm);
                                # 20.0 falls in the 0.18 mm gap between two knuckles. DrJones suggests this test.
