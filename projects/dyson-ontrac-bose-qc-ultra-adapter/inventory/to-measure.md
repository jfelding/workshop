# To measure

Calipers, in mm. Measured values are in `cad/measurements.py`. v2 prints and works without these; each would
tighten a number that is now a photo reading or a calculation.

| Name in measurements.py | What | How | Matters for |
|---|---|---|---|
| `LATCH_FOOT_BEHIND_WALL_DEG` (-2.8, -2.8) | where the cushion really stops, against the calculated home (the first latch print says 1 to 2 degrees before it) | with the adapter in a cushion and twisted home: look through a short slot from the cushion side and measure the gap between the slot's closed end and the hook's stem (calculated 2.4 mm of arc at home) | the 1 to 2° of play before the teeth catch; with the true stop the teeth can sit right at it |
| `TWIST_TRAVEL_DEG` (16) | drop-on to home | mark the cushion and the plate, drop on where the hooks first go flat, twist to the stop, read the angle (or the arc at the cushion edge) | the latch sweep and picture only |
| `RING_OUTER_RADIUS` (41.1, from a photo) | outer edge of the cushion's hard black back ring, where it meets the foam | outside jaws across the ring at its widest and at 90 degrees to that, halve | plate edge (`COVER_RADIUS`, 0.4 mm beyond). The print covers it, so only if the ring shows |
| `PLA_MODULUS_ASSUMED_MPA` (2500) | stiffness of the printed arm | press a printed tooth down with a kitchen scale; 3.3 N (about 335 g) is the calculated value | reported forces only, no geometry |
