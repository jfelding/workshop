# To measure

Calipers, in mm. Measured values are in `cad/measurements.py`. Current design: hanging collar (concept 6).

| Name in measurements.py | What | How | Needed for |
|---|---|---|---|
| `BRACKET_RING_FRONT_WIDTH` | metal between the hole and the ring's front edge | outside jaws, hole edge to front edge | the collar assumes the front is a half circle around the hole, i.e. the same 8.65 as at the sides |

Checked by the first print, not by calipers: the thread fit on the clear neck (pitch about 3.25 was hard to
measure; thread clearances are provisional).

Not needed for the collar: the black pump's inner thread (`exports/pump_c_gauge.stl` measures it if a
screwed-on pump is wanted later). Parked with the white-pump route: `PUMP_B_*`, `NARROW_NECK_ROOT_OD`,
`NARROW_NECK_THREAD_PITCH`, `NARROW_NECK_HEIGHT`. Later: the amber glass body's neck.

## Amber glass bottle holder (concept 7), 2026-11-22

The holder (`cad/amber_holder.py`) is modelled from **estimates**, at Jacob's request, to be printed and
tried. The estimates are the `EST_*` names in `cad/measurements.py`, each with its source and range. Replace an
estimate by a measured name when it is measured. Calipers and a ruler, in mm, with the bottle and pump in hand:

| Estimate in measurements.py | What | How | Matters for |
|---|---|---|---|
| `EST_AMBER_BODY_OD` (65) | glass body diameter, widest point | outside jaws, at base and at shoulder | the holder takes 62 to 68; outside that, the spine or lip moves |
| `EST_AMBER_HEIGHT_NO_PUMP` (110) | table to neck top, pump off | ruler | where the collar is, so where the ring sits; checked at 107 and 113 |
| `EST_AMBER_BODY_STRAIGHT`, `EST_AMBER_SHOULDER_TOP` (82, 94) | table to where the shoulder starts, and to where it meets the neck | ruler, or a photo from the side next to a ruler | whether the shoulder lifts the ring; the ring is fine either way |
| `EST_PUMP_C_COLLAR_HEIGHT` (17) | pump C's collar, outside height | outside jaws | the ring must sit round the collar or the neck below it |
| `EST_PUMP_C_HEAD_TOP`, `EST_PUMP_C_HEAD_OD`, `EST_PUMP_C_SPOUT_REACH`, `EST_PUMP_C_STROKE` | table to head top with pump on; head width; axis to spout tip; how far the head goes down | ruler | only the stand-in in the checks; the holder stays 28 mm below the pushed-down head |
| `EST_AMBER_NECK_THREAD_OD`, `EST_AMBER_NECK_UNDER_COLLAR_OD` (43, 40) | neck over the thread, and just below the collar | outside jaws, pump off | nothing in the holder; the ring is sized from the measured 52.0 collar |
| `EST_AMBER_HEEL_RADIUS` (4) | rounded bottom edge of the glass | photo of the base from the side | clearance to the 2 mm chamfer where foot meets spine |

After the first print, check on the real thing, in this order:

1. Does the ring go over the pump head? If not, put it on with the pump off. Does it turn freely round the collar's base?
2. Does the key slide into the channel from the top without force, and drop to the floor? Too tight: file the
   key's flanks. Too loose: it only rattles; leave it.
3. Bottle standing on the foot: gap between the glass and the spine (designed 4.5), and between the glass and the
   lip (4.5). Is the ring round the collar or the neck, and not lifted off the channel floor by the shoulder (designed 8 mm gap)?
4. Push the top of the bottle forward: it should stop after about 2 mm. Push the base forward: about 5 mm.
5. Lift to take it out: designed 25 mm. Is there room above the bottle where it hangs?
6. Pump it twenty times hard. Any creak or movement at the foot or the glue line?

Seller figures used for the estimates (foroils.com, Amazon B08YY5183S, an Alibaba factory listing), not
measurements: body 64-65 mm, height without pump 110 mm, with pump 165 mm, "neck" or "opening" 43 mm (inner or
outer is not stated; one seller says 45), glass about 3 mm.
