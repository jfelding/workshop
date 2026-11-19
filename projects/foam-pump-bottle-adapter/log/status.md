# Status

2026-11-19. Design: hanging collar (concept 6) for the black pump (C) on the clear square bottle.
`cad/hanging_collar.py` builds a draft (`--draft`): one valid solid, a plain ring 57.0 mm across and 17.7 mm tall, 16.4 cm³, zero
overlap with the neck core, the clamped ring and the pump body; web 2.95 mm at the front. Pictures of it in place: `exports/preview.png`, `exports/view-*.png` (`cad/illustrate.py`).

Draft because:
- `BRACKET_RING_FRONT_WIDTH` is not measured; the draft assumes a half-circle front.
- Printed bottle threads are not in `workshop.fits`; thread clearances are provisional and the clear neck's
  pitch (about 3.25) is a rough reading. The first print is the measurement.
- Fits used are the PLA ones. Not printed yet.

Parked: white pump on the brown bottle (concepts 1/2). Superseded: concept 5. Out: concept 3.
