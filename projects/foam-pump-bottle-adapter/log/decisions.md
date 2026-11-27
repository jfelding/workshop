# Decisions

## In force

| Date | Decision |
|---|---|

| 2026-11-19 | Black pump (C) on the clear square bottle, held by the hanging collar (concept 6). The pump is not screwed on; it rests on the collar's lips. Chosen because it needs one printed thread and no measurement inside the pump's collar. |
| 2026-11-22 | Pump C goes on its own amber glass bottle, held by our own printed wall holder (concept 7, hidden holder), not on the old metal bracket. Chosen because the pump and bottle then screw together as made, and nothing needs an adapter thread. Glass is carried from below by a foot, with a loop under the pump collar so it cannot be pulled out forward. The clear-bottle hanging collar (concept 6) stays as the fallback. |
| 2026-11-22 | Amber holder modelled from estimates (Jacob: print, test, adjust), not from measurements. Estimates live in a separate `EST_*` block of `measurements.py`. |
| 2026-11-22 | The closed loop of concept 7 becomes a loose ring with a dovetail key. The ring goes round the base of the pump collar (bore 55, from the measured 52.0 collar), the key drops into a channel at the top of the spine. Why: a loop fixed to the spine can only be entered by tilting the bottle in, which needs the unmeasured neck length and diameter to be right within a few mm; the loose ring needs neither, and the checks pass for bodies 62-68 and heights 107-113. The bottle goes in with the pump on: lower it with the key into the channel; take it out by lifting 25 mm. |
| 2026-11-22 | The holder prints on its side (one 30 mm wide profile), so spine, foot and the corner between them all lie in the layers and the foot's bending never pulls layers apart. The ring prints upside down, flat, with the key standing up. No supports. |
| 2026-11-22 | Amber holder sized by beam hand-calcs (`cad/amber_strength.py`) for 6 N bottle + 30 N push and a 20 N knock, SF 3 or more against PLA 45 MPa along / 25 MPa across the layers. The ring went from 3 × 4 to 4 × 5 mm (SF 1.5 to 3.2). The 15 mm brace under the foot was dropped: the plain 8 mm root has SF 3.7 counting the inside corner (Kt 1.5), and Jacob wants it slim. |
| 2026-11-22 | No screw holes: Jacob glues the holder to the wall with construction adhesive (montagelim). The flat 30 × 109 mm back is the glue pad; peak tension 0.077 MPa under the design loads. Jacob offered a wider back plate; not taken, because the numbers do not need it and wings wider than the 30 mm profile would leave the foot hanging in the air in the side-on print (supports). If it ever does need more glue area, make the spine taller below the foot instead. |

## 2026-11-24 Ring on the neck under the collar (amber holder v2)
Jacob's suggestion. The ring goes over the glass thread with the pump off and sits on the 17 mm of bare neck; the
screwed-on collar keeps it there and it is the collar's width, so it does not show. It no longer depends on the
pump's outside shape. Cost: the pump has to come off once to fit it, and the bore has only 0.25 mm radial
clearance over the glass thread (a running fit from `workshop.fits`, measured on a 6 mm pin, not on a 44 mm bore).

## 2026-11-26 Ring v3 from photo estimates, flat underside
Jacob would rather print a few times than measure the neck profile, so the ring's bore follows
`EST_AMBER_NECK_PROFILE` (from his photos) with 1 mm of upward margin for the estimate's error. Nothing of the ring
hangs below its underside inside the body outline (the v2 brace and web drop hit the domed shoulder), so the shoulder's
shape below the ring cannot clash, whatever it is.

## 2026-11-26 Ring v4: neck traced from close-ups, shorter and wider ring
Jacob's two close-ups of the bare bottle show no band under the thread: the neck runs straight to about 3 mm below the
collar and then the shoulder rounds out (about 51 across 7 below). A 52.5 ring 6 mm tall cannot sit there, so the ring
is 4.5 tall with a 5 mm wall (54.5 across, 1 proud of the collar). It only stops the bottle moving forward (the bottle
stands on the foot), so its height matters only for hoop strength, which went up (height × wall² 112 against 96).
Bore follows the traced profile plus 1 mm upward margin. Printed top down, the bore widens away from the bed: no overhang.

## 2026-11-26 Ring v5: calibrated on the v4 fit, 2 mm taller
v4's key fitted perfectly, but with the pump on the bottle lifted 2.0 before the shoulder caught the ring (model 1.25)
and felt loose. Jacob suggested 2 mm more ring. The ring now reaches 2 mm further down the shoulder; the 0.75 difference
is taken as a calibration of the traced profile (`EST_AMBER_NECK_PROFILE_DROP`) and the upward margin cut from 1.0 to
0.3, so the modelled lift is 0.5. Wall 5.5 (55.5 across) keeps 1.95 at the thin underside. The hoop check now sums the
tapered section instead of taking the thinnest wall over the full height.

## 2026-11-26 Shim under v4 before reprinting the ring
A 6 minute shim tests v5's calibrated shoulder fit on the v4 ring Jacob already has (its key fits perfectly). Print v5
only if the shim fails or the stack feels wobbly.

## 2026-11-27 Split ring instead of a screwed-on ring
The bore must pass the 44.0 thread, leaving 0.5 radial play on the 43.5 neck. A slotted ring springs over the thread
and closes on the neck with no new measurements; a ring screwed past the thread would need the glass thread's pitch,
depth and start, all unmeasured. Gauge first, since no split-ring grip fit is characterised.
