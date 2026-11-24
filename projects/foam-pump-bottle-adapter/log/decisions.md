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
