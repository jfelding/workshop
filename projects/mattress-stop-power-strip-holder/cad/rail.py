"""The T-slot profile the adapters' feet sit in (holder_side.slot), and the T-foot itself.

Profile (Y towards the room, measured from the front face of the back plate):
  RAIL_BASE   solid floor of the slot
  UNDER_D/W   the undercut the foot's head sits in
  LIP_T       the lips the foot's head hooks behind; the strip's back rests on their front face
  SLOT_W      the opening between the lips
"""
from build123d import *

RAIL_BASE = 1.8                     # solid floor of the slot
UNDER_D, UNDER_W = 2.6, 11.0
LIP_T, SLOT_W = 2.0, 6.0
RAIL_H = UNDER_W + 2 * 3.5          # 3.5 mm of lip on each side of the undercut
RAIL_T = RAIL_BASE + UNDER_D + LIP_T
# the foot that runs in it
FOOT_L = 20.0                       # long, so the adapter can't rock in the slot
FOOT_CLR_D, FOOT_CLR_W = 0.3, 0.5   # play in depth and in height (on the total)
NECK_CLR_W = 0.4
FOOT_CHAMFER = 0.8                  # lead-in at the foot's ends


def foot(length=FOOT_L):
    """The T-foot in the adapter's frame: Z = 0 is the rail's front face (= the strip's back),
    the foot hangs below it (Z < 0); X along the slot, Y across it."""
    head_t = UNDER_D - FOOT_CLR_D
    head = Box(length, UNDER_W - FOOT_CLR_W, head_t, align=(Align.CENTER, Align.CENTER, Align.MAX)).moved(
        Location((0, 0, -LIP_T)))
    neck = Box(length, SLOT_W - NECK_CLR_W, LIP_T, align=(Align.CENTER, Align.CENTER, Align.MAX))
    f = head + neck
    return chamfer(f.edges().filter_by(Axis.Y).group_by(Axis.X)[0] + f.edges().filter_by(Axis.Y).group_by(Axis.X)[-1]
                   + f.edges().filter_by(Axis.Z).group_by(Axis.X)[0] + f.edges().filter_by(Axis.Z).group_by(Axis.X)[-1],
                   FOOT_CHAMFER * 0.5)
