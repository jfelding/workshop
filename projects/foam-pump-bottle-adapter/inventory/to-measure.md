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

## Amber glass bottle holder (concept 7), v2 2026-11-24

The bottle was measured on 2026-11-24 (`cad/measurements.py`). The estimates left (`EST_*`) only shape the stand-in
used by the checks: where the body's straight side ends, the glass heel, the pump head. None of them moves the
printed parts. Nothing more to measure before printing.

After printing v2, check on the real thing, in this order:

1. Pump off: does the ring go over the glass thread (44.0, bore modelled 44.5)? If tight, sand or scrape the bore;
   do not force it on glass. Pump back on: the ring should turn freely under the collar.
2. The key is printed 0.1 mm per side oversize and 0.5 mm long. File its flanks until it slides into the channel
   from the top without force and does not wobble; file its bottom end if the ring sits higher than you want.
3. Bottle standing on the foot: about 1.5 mm of air between the glass and the spine, and the same at the lip.
4. Push the top forward: it should barely move (under 1 mm). Lift to take it out: about 20 mm.
5. Pump it twenty times hard. Any creak or movement at the foot or the glue line?
