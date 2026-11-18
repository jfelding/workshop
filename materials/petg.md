# PETG

**Status: one outcome recorded (bed adhesion); no fits measured.** It is the material for parts that must flex
(snap hooks, clips, living hinges). It is tougher and less stiff than PLA, and strings more.

- Profile: `equipment/neptune-3-pro/profiles/petg-pro-fast-0.4`. This is Elegoo PETG PRO at
  230 °C nozzle / 70 °C bed, with an 8 mm³/s volumetric limit. The part fan is off for the
  first 3 layers, then runs at 50–100 %.
- 2026-11-16/17: thin rings (78 × 97 mm, 2 mm plate) for the Dyson/Bose ear-cushion adapter lifted off the
  textured PEI bed twice in PETG with this profile. The same parts in PLA printed fine and the PLA hooks
  were springy enough, so the adapter stayed PLA. Whoever prints the next PETG part should record:
  - hole shrink on a known bore;
  - whether the part releases cleanly from PEI;
  - stringing.

  Then fill in `fits.md` and `fits.py`.
- PETG can bond to bare smooth PEI hard enough to tear the sheet. The textured sheet is safer.
  This is general knowledge, not seen here.
- A fit measured in PLA does not carry over to PETG.
