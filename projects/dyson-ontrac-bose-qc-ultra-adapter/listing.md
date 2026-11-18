# Printing-site listing

The text, files and settings used for this project's page on Printables, MakerWorld and Thingiverse.
Change it here first, then update each site; the pages that exist are in `publish-state.json`.

| Field | Value |
|---|---|
| Title | Dyson OnTrac ear cushions on Bose QuietComfort Ultra headphones (adapter) |
| Summary | Twist-lock adapter that fits Dyson OnTrac ear cushions to Bose QuietComfort Ultra headphones. Nothing is modified. |
| Licence | Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0), because the listing includes the Bose half |
| Remix of | https://makerworld.com/en/models/529246-bose-quietcomfort-ultra-earpad-frame (Dr. Watt, CC BY-NC-SA) |
| Category | Printables: Gadgets > Audio. Elsewhere the closest to audio or headphone accessories |
| Tags | dyson, ontrac, bose, quietcomfort, headphones, earpads, cushions, adapter |
| Price | Free |
| AI used | Yes, AI-assisted: the code-CAD was written with an AI agent; measured, printed and fitted by hand |

## Files, in this order

Model files, from `exports/` after `./check.sh`:

1. `dyson_half.stl` (print 2)
2. `bose_half.stl` (print 2)
3. `dyson_half.step`

Pictures, the first is the cover:

1. `images/worn-pair.jpg`
2. `images/on-earcup.jpg`
3. `images/adapter-in-cushion.jpg`
4. `exports/preview.png`
5. `exports/dyson_half.png`
6. `exports/bose_half.png`

## Print settings fields

| | |
|---|---|
| Printer | Elegoo Neptune 3 Pro |
| Material | PLA |
| Nozzle | 0.4 mm |
| Layer height | 0.2 mm |
| Supports | No |
| Time | About 25 minutes per part, 100 minutes for a full set of four |
| Weight | 5.9 g + 5.7 g per ear, about 23 g for a full set |

## Description

My Bose QC Ultra (1st gen) headphones needed new earpads, and a local store was selling leftover Dyson
OnTrac earpads for 15 ¢ (0.15 EUR). So I made an adapter and glued it onto the Bose earpad frame that
this is a remix of. Thanks to Dr. Watt for that part.

The adapter is two flat prints glued back to back: one half clips into the Bose earcup, the other has
four hooks that the Dyson cushion twists onto. I made it as two glued parts rather than one because it
has hooks on both sides; this way each half prints flat with no supports.

Nothing on the headphones or the cushions is modified, and the original Bose cushions go back on at any
time. Printed and in daily use since November 2026. Source and details:
https://github.com/jfelding/workshop/tree/main/projects/dyson-ontrac-bose-qc-ultra-adapter

### What to print

Print **two of each** part, one pair per ear. Left and right are identical.

- `dyson_half.stl`: 78.0 × 96.5 × 4.7 mm, 5.9 g
- `bose_half.stl`: 78.0 × 96.5 × 5.0 mm, 5.7 g

You also need about 20 mm of 1.75 mm filament (four alignment pins) and superglue.

### Printing

- Printed in Bambu Nebula PLA on an Elegoo Neptune 3 Pro: 0.4 mm nozzle, 0.2 mm layers, 210 °C nozzle,
  60 °C bed, textured PEI, 4 walls, 20 % gyroid infill, 60 mm/s outer walls.
- Both parts flat side down, as the files come. No supports, no brim. About 25 minutes per part.
- PETG lifted off the bed twice at this size, so I stayed with PLA.
- PLA softens at about 55 °C, so do not leave the headphones in a hot car.

### Assembly

1. Cut four pins of 1.75 mm filament, about 4 mm long.
2. Push two pins into the two small pockets on the flat side of a Bose half. They are a press fit.
3. Put a thin line of superglue around the flat side of the Bose half.
4. Lower a Dyson half onto it, flat side to flat side, with the pins going through its two holes. The
   pins and the flush outer edges line the halves up. Either way round is correct. Press for a minute.
5. Snip the pins flush on the hook side.
6. Fit the cushion to the adapter first: lay the cushion on the hooks, find the position where it drops
   flat, and twist it clockwise (seen from the hook side) by about 16° until it stops.
7. Pull the original cushion off the Bose earcup and press the adapter in until its clips snap.

To take it off, pull the adapter out of the earcup like a normal Bose cushion.

### How the lock works

The back of a Dyson cushion has four curved slots, each with a ledge over one end. Each hook drops into
the open part of a slot, and twisting slides its lip under the ledge. The gap under the lip narrows from
1.4 mm to 0.8 mm, so the cushion is pulled down and clamped as it turns. There is no rattle and no
separate catch.

### If I printed it again

I would make the Dyson half a bit wider at the sides. It does not fully cover the middle part of the
cushion's lock ring, at the left and right of each earpad. It works fine as it is; this is only looks.

### Source and tuning

The CAD source (Python, build123d), every dimension, the checks and a table of what to change if your
fit differs are on GitHub:
https://github.com/jfelding/workshop/tree/main/projects/dyson-ontrac-bose-qc-ultra-adapter

### Credits and licence

- The Bose half is a remix of "Bose QuietComfort Ultra earpad frame" by Dr. Watt
  (https://makerworld.com/en/models/529246-bose-quietcomfort-ultra-earpad-frame), licensed CC BY-NC-SA.
  Change made: two pin pockets in the flat back.
- This listing is therefore CC BY-NC-SA 4.0. The Dyson half is my own design and is also available
  under CC BY 4.0 from the GitHub page above.
- Not affiliated with or endorsed by Dyson or Bose. Their names are used only to say what the part fits.
