# To measure

Calipers, in mm. Measured values are in `cad/measurements.py`. Current design: the amber holder (concept 7, below). The table is for the fallback hanging collar (concept 6).

| Name in measurements.py | What | How | Needed for |
|---|---|---|---|
| `BRACKET_RING_FRONT_WIDTH` | metal between the hole and the ring's front edge | outside jaws, hole edge to front edge | the collar assumes the front is a half circle around the hole, i.e. the same 8.65 as at the sides |

Checked by the first print, not by calipers: the thread fit on the clear neck (pitch about 3.25 was hard to
measure; thread clearances are provisional).

Not needed for the collar: the black pump's inner thread (`exports/pump_c_gauge.stl` measures it if a
screwed-on pump is wanted later). Parked with the white-pump route: `PUMP_B_*`, `NARROW_NECK_ROOT_OD`,
`NARROW_NECK_THREAD_PITCH`, `NARROW_NECK_HEIGHT`. Later: the amber glass body's neck.

## Amber glass bottle holder (concept 7), ring v5, 2026-11-26

Jacob chose not to measure further: ring v5 is built on `EST_AMBER_NECK_PROFILE` (traced from his close-ups of the bare bottle) and corrected by
test prints. A measured `AMBER_NECK_PROFILE` (neck OD at 0, 2, 4 ... mm below the collar, pump on) or a caliper reading
of the filed v2 key would still replace the estimates if anyone takes them. `AMBER_NECK_BARE_HEIGHT` (17) is doubted
and no longer shapes the ring.

After printing ring v5, check on the real thing, in this order:

1. Pump off: does the ring go over the glass thread (bore 44.5 at the top)? If tight, sand the bore; do not force it.
2. Pump on, screwed tight: does the ring sit level round the neck, not rocking, with its underside just clear of the
   shoulder? Lift the bottle: it should rise about 0.5 mm before it catches the ring (v4: 2.0). If the shoulder
   lifts the ring against the collar, raise `NECK_PROFILE_MARGIN_UP` by the overlap; if it still lifts more than 1, lower it.
3. The key has 0.15 mm play per side and is 0.5 mm long: it should slide into the channel without filing and not
   wobble. File its bottom end if the ring sits higher than you want.
4. Bottle standing on the foot: about 1.5 mm of air between the glass and the spine, and the same at the lip.
5. Push the top forward: it should barely move (under 1 mm). Lift to take it out: about 20 mm.
6. Pump it twenty times hard. Any creak or movement at the foot or the glue line?
