# PETG

**Status: small parts printed (coupon and fit slice, 2026-11-27). Large first layers took some work; see
below.** It is the material for parts that must flex (snap hooks, clips, living hinges). It is tougher and less
stiff than PLA, and strings more.

## How to print PETG on the Neptune 3 Pro

This is the routine that got PETG to stick on the smooth PEI sheet (2026-11-27, the user; it was worked out on
a monitor wall-mount spacer, an 84 × 73 mm first layer).

1. **Profile:** `equipment/neptune-3-pro/profiles/petg-smooth-pei-0.4-adaptive-purge`. It sets the bed to
   85 °C on layer 1 and 80 °C after, and the nozzle to 240 °C on layer 1 and 235 °C after. It also retracts on
   every travel, including inside infill (`reduce_infill_retraction` off), so the nozzle does not ooze across the
   part and collect PETG. Slice at stock speeds. Use the G-code it makes; don't change temperatures on the printer.
2. **Level the bed hot:** heat it to 80 °C, wait about 5 minutes, then run the auto-level from the screen. A
   mesh made at PLA temperature does not match the hotter bed.
3. **Clean the sheet:** wash it with warm water and dish soap to remove old glue, then dry it.
4. **Glue stick, thin:** rub it lightly over the part's area, then spread it with a damp, wrung-out cloth or
   paper towel until only a faint haze is left. White streaks are too much: the PETG floats on them and peels
   up onto the nozzle. The glue also keeps PETG from bonding to bare smooth PEI, which can tear the sheet.
5. **Wipe the nozzle while it is hot** before every print. Old PETG on it picks up more and drops blobs.
6. **Z-offset:** do not raise it to cure lifting. Less squish means less grip. If corners lift, lower it
   0.02–0.03 mm at a time.
7. **For a large part, print a few first layers as a test** (about 15 minutes) before committing hours.

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
- **Smooth PEI with glue stick: worked for PETG** (2026-11-27, coupon plate,
  `petg-pro-fast-0.4-adaptive-purge`, bed 70 °C). The user put glue stick on the smooth PEI sheet; the first
  layer held, and so far the print is fine. The glue is a release layer as well as adhesion, so PETG does not
  bond to the bare PEI. Whether the parts come off cleanly is not yet recorded. This is for PETG on
  smooth PEI only; it says nothing about PLA or the textured sheet.
- **Large first layers on smooth PEI + glue are harder** (2026-11-27, monitor-mount spacer, 84 × 73 mm). At 70 °C
  bed and 230 °C, with thick, streaky glue, the bottom fill peeled up as a sheet onto the nozzle. Thick glue
  floats the PETG; raising Z made it worse. What the user then found works better: spread the glue with a
  damp, wrung-out cloth to a faint haze, bed 85 °C on layer 1 and 80 °C after, nozzle 240 °C on layer 1 and
  235 °C after. Some random blobs remained. Profile `petg-smooth-pei-0.4-adaptive-purge` sets these, plus a
  0.95 first-layer flow (untested).
- **Random blobs on upper layers, dry filament** (2026-11-27, monitor-mount spacer, Elegoo-based PETG profiles). Not
  over-extrusion: the G-code already extrudes 0.95 of nominal above layer 1 (process 0.97 × filament 0.98,
  checked from E per mm on the walls). Suspect: `reduce_infill_retraction` = 1 (Orca stock), so ~1,500 travels
  per spacer cross the infill with no retraction and no Z-hop. The oozing nozzle drags through the part, PETG
  builds up on it and drops off as blobs. OrcaSlicer's wiki warns the setting may increase oozing inside
  infill. Now off in `petg-smooth-pei-0.4-adaptive-purge`, the standard PETG profile; turn it off in any PETG
  profile. Not yet confirmed by a print. If blobs remain, try 230 °C after layer 1 next.
- A fit measured in PLA does not carry over to PETG.
