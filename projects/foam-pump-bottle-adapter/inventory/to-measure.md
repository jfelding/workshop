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
