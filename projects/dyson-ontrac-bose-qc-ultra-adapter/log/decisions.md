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

## 2026-11-22 Wide Bose half as a separate part, rim from the Dyson outline function
Chosen: `bose_half_wide` adds a rim only outside the frame's oval and imports `dyson_half_wide.outline()`, so the two
halves cannot drift apart; the proven `bose_half` and the vendor mesh are untouched. Rim thickness equals the frame
plate (2.0), chamfered 0.3 like the Dyson half because the frame's own wall is a sharp vertical one and the rim is
free-standing at the sides. Wide pairs with wide only. Licence: remix of the frame, so CC BY-NC-SA like `bose_half`.

## 2026-11-23 Lock by a spring pawl in the short slots, not by a bump
Chosen: a flexure arm with a tooth that drops into each short slot behind its closed end. The wedge leaves the cushion
no lift near home, so the moving part has to be in the adapter. The short slots are used because their closed end
passes over plain plate during the twist, with 13.7° to the nearest hook.
Chosen: release by twisting back (lock face 62°), not by a release tab: the tooth is hidden under the cushion once on.
70° is the limit, above it friction can make the tooth self-locking.
Chosen: teeth staggered at -0.7° and +0.9° from the calculated closed-end position, because the true stop is unmeasured.
Costs up to about 1.7° of play; to be removed after one print tells which tooth holds.
Chosen: new `bose_half_latch` with blind pockets rather than a thicker Dyson half: the stack stays 9.7 mm.
Rejected: a taller rigid bump (cannot be passed), a radial snap on the ring's edge (ring radius is photo-read).
