# Status

2026-11-24. Main design: our own wall holder for the amber glass bottle with the black pump (C), concept 7,
**holder v2 printed 2026-11-26; ring v4 printed (key perfect, bottle loose); next: a 2 mm shim under v4 (`cad/amber_shim.py`, sliced), or ring v5 (sliced).** The first print (from seller estimates) was too roomy and its ring
sat round the neck instead of the collar. Two printed parts, `cad/amber_holder.py`:

- holder: spine, foot and front lip, one 30 mm wide profile, 112 × 81 × 30 mm, 47.2 cm³, printed on its side.
  1.5 mm of air round the measured 65 mm body. Dovetail channel roof now 60° from flat (was 50°, printed ragged).
  No holes: glued to the wall with montagelim.
- ring: sits on the bare glass neck (43.5) just under the pump collar, 6.5 mm tall, top 1 mm under the collar,
  55.5 across. Fitted with the pump off. A solid trapezoid web joins the ring to the key and bears on the spine face
  0.5 mm away; nothing hangs below the ring's underside. The bore is 44.5 over the straight neck and then follows the
  shoulder (`EST_AMBER_NECK_PROFILE`, traced from close-ups with the perspective corrected, plus a 0.75 mm drop
  calibrated on the v4 fit) with 0.3 mm upward margin, so the bottle lifts about 0.5 before the shoulder catches the
  ring. Wall 1.95 at the underside. Key: 0.15 per side play, 0.5 long (perfect fit on v4). Print at 100% infill. 7.4 cm³,
  hoop SF 7.6 (tapered section summed). v5 sliced: `scratch/amber5_ring-20261126/plate_1.gcode`, 37 min, 9.0 g.
  History: v3 assumed a band that does not exist; v4 (4.5 tall, 1.0 margin) fitted but the bottle lifted 2.0 and felt loose.

`./check.sh` passes: zero overlap installed and on the way in and out; bottle moves 0.5 mm forward at the top and
1.75 at the base before it stops, and lifts 0.5 before the shoulder catches the ring; lowest safety factors 3.9 (foot root), glue SF 6.9.
Numbers in `exports/checks-amber.json` and `checks-amber-strength.json`.

Fallback, unchanged: hanging collar (concept 6) for pump C on the clear square bottle, draft, `cad/hanging_collar.py
--draft`; its pictures are `exports/view-*.png`. Draft until `BRACKET_RING_FRONT_WIDTH` is measured.

Parked: white pump on the brown bottle (concepts 1/2). Superseded: concept 5. Out: concept 3.
