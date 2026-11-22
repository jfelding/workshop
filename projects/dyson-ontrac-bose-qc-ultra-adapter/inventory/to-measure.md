# To measure

Calipers, in mm. Measured values are in `cad/measurements.py`. Everything below is currently a **best guess read
from a photo** (2026-11-22, approved by the owner for the detent test variant only, `dyson_half_detent`). Replace
each by a measured value and the variant rebuilds.

| Name in measurements.py | What | How | Matters for |
|---|---|---|---|
| `LEDGE_BARS_PHOTO` start/end angles (7.5-22.8, 98.5-112.3, 187.5-203.2, 277.5-293.6 in photo frame) | where each ledge bar starts (lock end) and ends | with calipers, the bar's length along the slot's outer edge (chord, end to end), and its distance from the slot's closed end; bars look about 10 mm (long) and 9.5 mm (short) | where the bump sits under the bar |
| `LEDGE_BARS_PHOTO` inner radius (38.1, 37.8, 37.7, 37.9) | bar inner face | depth gauge or jaws: distance from the slot's outer edge to the bar's inner face (about 1.2-1.6 mm) | bump radial position (kept inside 38.2-39.0) |
| `LEDGE_BARS_PHOTO` outer radius (39.3) | bar outer face | taken as the slot's outer edge, `SLOT_OPPOSING_SPAN` / 2; check the bar is flush with it | same |
| `PHOTO_FRAME_OFFSET_DEG` (47.5) | turn of the photo against `SLOT_ANGLES` | only exists because of the photo; disappears once bar angles are measured in the `SLOT_ANGLES` frame | all four bars |
| `TWIST_TRAVEL_DEG` (16) | drop-on to home | mark the cushion and the plate, drop on where the hooks first go flat, twist to the stop, read the angle (or the arc at the cushion edge) | where the bar is relative to the bump at drop-on |
| `LEDGE_THICKNESS_ASSUMED` (0.8) | thickness of the slab the hook lip clamps | jaws across the ledge under the bar, or a feeler gauge | how much the cushion can lift at the crest: the 0.065 mm margin moves 1:1 with this |
| `LEDGE_PROTRUSION` (0.6, measured) | bar height above the cushion face | re-measure if bumps seem to do nothing | clearance over the relief, now 0.2 mm |
| `RING_OUTER_RADIUS` (41.1) | outer edge of the cushion's hard black back ring, where it meets the foam | outside jaws across the ring at its widest and at 90 degrees to that, halve (it read circular, 41.0-41.4 at twelve angles; uncertainty about 0.4) | `COVER_RADIUS` of `dyson_half_wide`: plate edge, 0.4 mm beyond |
