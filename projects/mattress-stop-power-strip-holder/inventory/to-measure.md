# To measure

Values the CAD still takes from a photo or an estimate. Measure them before the next reprint.

| Constant | Where | What | How | Blocks |
|---|---|---|---|---|
| `HEAD_ARM_W` (via the plus's arm neck, ~2.8) | `cad/adapter.py` | width of each arm of the strip's plus hole at its narrowest | feeler gauge or drill shanks through the arm | the adapter head width (test heads 2.2/2.6 cover it meanwhile) |
| slot spacing error (~5 mm) | printed holder | how much closer together the printed T-slots are than the strip's plus holes | calipers: slot centre to slot centre on the print, plus centre to plus centre on the strip | which offset adapter pair to use |
| `INS_BOT` (−50) | `cad/holder_mag.py` | how far down the pocket inside the stop's cloth cover goes | pull the cover half off and measure from the bar | insert height |
| `DRYFIT_D` (None) | `cad/remote_shell.py` | board underside above the front half's rim, in the dry fit | depth gauge, after printing the front half | `remote_back.stl` |
| `BOOT_D` (9.8) | `cad/remote_shell.py` | cable boot diameter where it leaves the case | calipers | slim case cable clamp |
| `SCREW_CLR`, `SCREW_PILOT` (3.2, 2.4) | `cad/remote_shell.py` | the original case screws (assumed ~2.9 mm self-tappers, Ø5.5 heads) | calipers on a screw | slim case screw holes |
| `CABLE_Z` (10) | `cad/strip.py` | height of the strip's cord above its base | calipers | nothing (the cord end is open) |
