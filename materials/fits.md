# Fits: how big to model a hole

The numbers `src/workshop/fits.py` uses, with the evidence behind each one. A fit belongs to a
**process** (machine × material × nozzle); it does not carry over to another process. Each row is
tagged as `measured` (calipered on a printed part), `in use` (built into parts that went together,
but never calipered) or `untested` (derived from a measurement, outcome not recorded).

The method stays the same whatever the process (`methods/cad-in-code.md`, "The loop"):

1. Model the fit from this table.
2. Print a **cheap real part** that carries it, not a coupon, and measure it.
3. Correct the table and `fits.py` together, adding the date and the part.
4. A hole that comes out tight is reamed by twisting a drill by hand. Reprint only when the
   geometry is wrong, not the size.

Slicer XY hole compensation stays at **0**. Every allowance lives in CAD, so this file and
`fits.py` are the only places that hold one.

## Neptune 3 Pro, PLA, 0.4 mm nozzle

**Small vertical holes print 0.2 mm under their modelled diameter.** A Ø5.5 bore measured Ø5.30
(Ø5.40 with the caliper pressed outward). Measured 2026-10-29.

The model diameter is `shaft + clearance + 0.2`. This is `hole_for(shaft, fit)`.

| Fit | Printed clearance (diametral) | Example | Evidence |
|---|---|---|---|
| `press` | −0.05 | Ø6.0 bore on a Ø5.85 LED flange | untested (LED caps v3, 10-29) |
| `slip` | +0.05 | Ø6.1 bore on a Ø5.85 flange | untested (LED caps v3, 10-29) |
| `running` | +0.3 | Ø6.5 pivot bore for a Ø6 steel pin | measured: prints ~6.3. Ø6.2 printed 6.0 and had to be drilled (head frame v2, 10-09) |

Other allowances for this process:

| What | Allowance | Evidence |
|---|---|---|
| Hex nut pocket, press | +0.15 across flats (AF), +0.3 depth. A thin M3 nut (5.2 AF × 2.1) goes in a 5.35 × 2.4 pocket | measured: fitted by hand, held (carrier v2, 10-13) |
| Hex nut pocket, clearance | +0.3 AF, +0.4 depth | in use |
| Self-tapping M3 pilot | Ø2.5 | in use: M3×8 and M3×20 held gear and stub retainers |
| Printed part sliding in printed part | 0.5 | in use |
| Printed part dropped into a printed pocket | 0.3 | in use |
| Flat sheet (metal) dropped into a printed seat, total per side length (`sheet_seat`) | 0.3 | untested. **0.2 is borderline:** a 70.2 × 20.2 seat took a 70 × 20 × 1 mm sheet on a flat 3.3 mm coupon, but needed filing on the full 20–31 mm holders printed with the 300 % speed override (sheet holders, 10-13). Confounded: height and speed both changed |
| Printed part sliding in a printed channel, 0.4 per side (0.8 total) | 0.8 | untested (breadboard mount, 10-14). **Too loose for a load-carrying dovetail:** a 16 mm key printed standing, in a 50° dovetail channel printed on its side, at 0.4 per side let the part it carried hang and tilt (foam-pump amber ring, 2026-11-24, by hand, not measured). Next version: key +0.1 per side oversize, filed to fit |
| Smallest gap between printed walls | 0.8 | measured: 0.3 mm gaps closed up and cheeks splayed into a gear (10-09) |
| Elephant-foot compensation (slicer) | 0.15 | in use |
| Floor under a blind tapped hole | more than 2 mm | measured: 2 mm was too thin |

**D-shaft bore (Ø5 stepper shaft, flat 4.5 AF).** Modelled at Ø5.355 with a 4.825 AF flat. It
still printed tight. Filing the shaft flat to 4.65 gave a firm press. The circle centres the
part and the flat only drives, so fit the flat and leave the circle alone. File by hand from
above and stop early.

## Neptune 3 Pro, PLA, 0.2 mm nozzle

Elephant-foot compensation is 0.10, and 0.10 mm layers hit heights exactly (4.50 mm spacers =
45 layers). Round heights **up** to a whole layer. One-wall dividers came out 0.22–0.27 mm.
Hole shrink has not been measured.

## Neptune 3 Pro, PETG, 0.4 mm nozzle

Profile `petg-pro-fast-0.4-adaptive-purge` (230 °C / 70 °C), smooth PEI with glue stick. From a monitor
wall mount's coupon plate, 2026-11-27. One print, so treat as a first number.

**Small vertical holes print about 0.15 mm under their modelled diameter.** The fit slice's Ø5.5 holes
measured about Ø5.35.

| What | Allowance | Evidence |
|---|---|---|
| Side-entry nut slot, tight (`slot_tight`) | +0.1 AF, +0.4 height. An M4 nut (7.0 × 3.2) in a 7.1 × 3.6 slot | measured: slid in by hand with effort |
| Side-entry nut slot (`slot`) | +0.3 AF, +1.0 height | untested; chosen from the tight one |

**Bridged slot ceilings sag.** The coupon's four slots (+0.1 to +0.4 AF, all +0.4 height) open sideways, with a
7 mm bridged ceiling. The three wider ones sagged more and the nut would not go in, so height, not width,
limited the fit. Hence `slot` adds 0.6 mm of height: a nut loose in a slot costs nothing, because the screw
pulls it up against the ceiling and the clamp flattens any sag. Slower bridges (Orca's `bridge_speed` is 40 mm/s
in the profile) and full fan might sag less; untried. Bottom-opening pockets (`press`, `clearance`) are not
measured in PETG.

## Not yet characterised

- **PETG** press and clearance fits, bottom-opening nut pockets, other nozzles.
- **Horizontal holes.** These print differently from vertical holes; use `workshop.cad.geometry.teardrop` and
  ream.
- **Heat-set insert bores.** This is the one case that deserves a coupon, because a drill cannot fix it.

## Standard sizes (not printer-specific)

ISO 273 medium clearance: M2 2.4, M2.5 2.9, M3 3.4, M4 4.5, M5 5.5, M6 6.6, M8 9.0
(`fits.clearance('M3')`).

Washers measure Ø14.5 for M5. Put a washer under every nut that bears on plastic: a bare M5 nut
on a printed lip gives about 157 MPa against a 30 MPa allowance for PLA, and a washer brings it to 23 MPa.
