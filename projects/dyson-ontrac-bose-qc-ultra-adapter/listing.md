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

Kept short on purpose; the details are in the README.

My Bose QC Ultra (1st gen) headphones needed new earpads, and a local store was selling leftover Dyson
OnTrac earpads for 15 ¢. So I made an adapter and glued it onto the Bose earpad frame that
this is a remix of. Thanks to Dr. Watt for that part.

It is two parts glued together rather than one, because it has hooks on both sides. Nothing on the
headphones or the cushions is modified.

### Printing

Print two of each part, flat side down, no supports. I used Bambu Nebula PLA on an Elegoo Neptune 3 Pro:
0.4 mm nozzle, 0.2 mm layers, 210 °C nozzle, 60 °C bed. About 25 minutes per part.

### Assembly

1. Push two 4 mm pieces of 1.75 mm filament into the pockets on the flat side of a Bose half.
2. Superglue a Dyson half onto it, flat side to flat side, with the pins through its holes. Snip the
   pins flush.
3. Twist the Dyson cushion clockwise onto the hooks, then clip the adapter into the earcup.

### If I printed it again

I would make the Dyson half a bit wider at the sides. It does not fully cover the lock ring at the left
and right of each earpad.

### Source and licence

CAD source, dimensions and more detail:
https://github.com/jfelding/workshop/tree/main/projects/dyson-ontrac-bose-qc-ultra-adapter

CC BY-NC-SA 4.0, because the Bose half is a remix of "Bose QuietComfort Ultra earpad frame" by Dr. Watt
(https://makerworld.com/en/models/529246-bose-quietcomfort-ultra-earpad-frame); I added two pin pockets.
The Dyson half on its own is CC BY 4.0 on GitHub. Not affiliated with Dyson or Bose.
