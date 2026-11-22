# Decisions

## 2026-11-22 Detent test variant uses photo-read ledge bars
Chosen: build `dyson_half_detent` from best guesses read from one photo, accepting a reprint, because
calipers were not to hand. The proven `dyson_half` is not changed. Values are in their own section of
`measurements.py` and in `inventory/to-measure.md`.
Chosen: bumps under the two long bars only (symmetric pair); 0.4 mm high (two layers; 0.2 would only graze the
0.2 mm clearance); crest 7° before home (the wedge gives no lift closer in); approach 20°, release 35°.
Rejected: a bump just behind the bar's trailing end at home (the bars are as long as the twist, so it would sit
under the bar at drop-on, and there is no axial slack at home).

## 2026-11-22 Wide plate as a separate test part, cover radius = ring + 0.4
Chosen: `dyson_half_wide` leaves `dyson_half` untouched; the detent test part is rebuilt on the wide plate. Outline =
oval united with a circle, 40 mm blend fillet (no corners). Cover radius = photo-read ring radius 41.1 + 0.4: the top
edge is rounded 0.6, so the flat face then ends at about the ring edge, and the reading is +/-0.4; pressing 0.4 mm
into the foam beyond the ring costs nothing. Bumps under the short bars not added: the wide plate gives them room
(2.2 mm to the edge) but the bar-as-long-as-the-twist problem is the same, so it stays a later test.
