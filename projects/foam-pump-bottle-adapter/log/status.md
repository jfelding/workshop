# Status

2026-11-22. Main design: our own wall holder for the amber glass bottle with the black pump (C), concept 7.
**Estimated dimensions, untested.** Two printed parts, `cad/amber_holder.py`:

- holder: spine, foot and front lip, one 30 mm wide profile, 109 × 87 × 30 mm, 47.2 cm³, printed on its side. Foot 8 mm
  at the spine to 5 at the lip, no brace; spine 10 mm; lip 3 × 6.
  No holes: glued to the wall with construction adhesive (montagelim).
- ring: goes round the pump collar's base (bore 55 for the measured 52.0 collar), 63 mm across (wall 4, height 5),
  with a dovetail key that drops into a channel at the top of the spine. 4.9 cm³, printed upside down.

`cad/amber_checks.py` (in `check.sh`) passes against a stand-in bottle built from the `EST_*` estimates: zero
overlap installed, along the way in and out (lift 25 mm, then forward), and with the pump head pushed down and
its spout turned front, side or to the wall; also for bodies 62-68 mm and heights 107-113 mm. Bottle stops
after 1.75 mm forward at the top and 4.75 mm at the base. Watertight STLs, no supports, nothing steeper than
45°. Strength (`cad/amber_strength.py`, 6 N bottle + 30 N push, 20 N knock, PLA 45 MPa along / 25 across the
layers): lowest safety factors 3.2 (ring hoop, along layers), 3.7 (foot root with Kt 1.5, along layers), 7.2 (key,
across layers); glue line 0.077 MPa, SF 6.5 against a deliberately low 0.5 MPa. Numbers in `exports/checks-amber.json` and `checks-amber-strength.json`; pictures `exports/preview.png`, `exports/amber-*.png`.

Fallback, unchanged: hanging collar (concept 6) for pump C on the clear square bottle, draft, `cad/hanging_collar.py
--draft`; its pictures are `exports/view-*.png`. Draft until `BRACKET_RING_FRONT_WIDTH` is measured.

Parked: white pump on the brown bottle (concepts 1/2). Superseded: concept 5. Out: concept 3.
