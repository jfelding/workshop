# Status

2026-11-24. Main design: our own wall holder for the amber glass bottle with the black pump (C), concept 7,
**version 2 from measurements, not printed.** The first print (from seller estimates) was too roomy and its ring
sat round the neck instead of the collar. Two printed parts, `cad/amber_holder.py`:

- holder: spine, foot and front lip, one 30 mm wide profile, 112 × 81 × 30 mm, 47.2 cm³, printed on its side.
  1.5 mm of air round the measured 65 mm body. Dovetail channel roof now 60° from flat (was 50°, printed ragged).
  No holes: glued to the wall with montagelim.
- ring: sits on the bare glass neck (43.5) just under the pump collar, bore 44.5 to pass the 44.0 thread, 52.5
  across (same as the collar, so hidden), 6 mm tall, top 1 mm under the collar. Fitted with the pump off.
  A solid trapezoid web (40 mm wide at the ring, 26 at the spine, 9 tall) joins the ring to the key and bears on
  the spine face 0.5 mm away; a 16 mm wide triangular brace under the web joins it to the key's lower end. Key printed
  0.1/side oversize and 0.5 long, filed to fit. Print at 100% infill. 8.2 cm³.

`./check.sh` passes: zero overlap installed and on the way in and out; bottle moves 0.75 mm forward at the top and
1.75 at the base before it stops; lowest safety factors 3.9 (foot root), 4.7 (ring hoop, key), glue SF 7.0.
Numbers in `exports/checks-amber.json` and `checks-amber-strength.json`.

Fallback, unchanged: hanging collar (concept 6) for pump C on the clear square bottle, draft, `cad/hanging_collar.py
--draft`; its pictures are `exports/view-*.png`. Draft until `BRACKET_RING_FRONT_WIDTH` is measured.

Parked: white pump on the brown bottle (concepts 1/2). Superseded: concept 5. Out: concept 3.
