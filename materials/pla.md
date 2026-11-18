# PLA

The default material in this shop. It is stiffer than PETG, warps less and strings less. Use PETG only
where a part must flex. Fits: `fits.md`.

## Stock and temperatures

- Elegoo PLA+ at **210 °C nozzle / 60 °C bed** on the textured PEI plate (polyetherimide, the
  printer's build sheet). This is within the maker's range and printed well (2026-10).
- Orca's default bed type is "Cool Plate", which gives a 35 °C bed. Set `curr_bed_type` to
  Textured PEI Plate.
- Thin PLA lets light through. Use black filament for light-tight caps and shrouds.
- Glitter PLA: keep the 0.4 mm nozzle, because a 0.2 mm nozzle may clog.

## What it is good and bad at

- **Layer direction.** Parts are weakest across layers. Orient a part so its load runs along the layer
  planes; this applies to pullers, clamps and cheeks. Add ribs on the outside faces so that bending
  stays within layers.
- **Infill.** Use gyroid. Rail and jaws: 25 % took 12 h 09 m for 110.6 g, 40 % took 16 h 38 m for 131.7 g.
  Lightning infill is not structural. Pullers and extractors: 6 walls, 60 % gyroid.
- **Bearing stress.** Allow 30 MPa under a nut, which means a washer under every nut on plastic.
- **Stiffness.** Beam theory predicts stiffness but does not prove it. Accept a part by a tap or creep test.
- **Creep.** PLA creeps under steady load and softens around 55–60 °C. Do not leave a printed
  part clamped hard near a heat source. This is general knowledge and has not been measured here.

## First layer

- Parts that print flat with fine detail on layer 1, such as gear teeth, print **interior first with no brim**.
  Orca 2.4.2 ignores `is_infill_first` on layer 1, so use
  `equipment/neptune-3-pro/reorder_first_layer.py`.
- Tall parts on a narrow footprint: use a 5 mm outer brim with a 0.15 mm gap. Brims of neighbouring parts
  touch and have to be cut apart.
- Put no brim under a flare, because the brim fuses to the overhang.
- Keep small footprints off worn patches of the PEI plate.
