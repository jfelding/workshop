# Lessons

Things that cost a print to learn. Add to the right heading, newest last, with a date and the project it
came from. Tags: **[M]** measured, **[C]** calculated, **[O]** observed once, **[U]** unverified (read
somewhere, not seen here).

## Snap and twist-lock hooks

- [O] 2026-11-17, Dyson/Bose adapter. **A sloped underside on a hook lip is a ramp, not a lock.** A 45° lip
  underside let the mating ledge slide straight back off. A flat land on the underside, at least 1 mm wide
  where the ledge bears, holds.
- [O] 2026-11-17, same. **A wedge needs somewhere to end.** A hook whose gap tapers from 1.4 to 0.8 mm along
  9 mm draws the part down as it turns and clamps it; without the taper the fit rattled, and with a taper
  that closed further it would not turn home.
- [O] 2026-11-16, same. **Do not let a plate rest on the feature it is meant to pass.** The mating part had
  blocks standing 0.6 mm proud of its face; a flat adapter plate sat on them and the hooks never reached.
  An open step (a lower plate outside a raised seat) cleared them.
- [M] 2026-11-17, same. A 10° undercut (barb) under a 1.5 mm lip sliced into islands starting in mid-air
  (`workshop.cad.printability.layers` shows them). Keep lip undersides flat or sloped the printable way.

## Gluing two prints back to back

- [O] 2026-11-17, same. Two pins cut from 1.75 mm filament line up two flat prints for gluing: a Ø1.95 hole
  in one part slips over the pin, a Ø1.85 blind pocket in the other grips it (0.4 mm nozzle, PLA).
- [O] 2026-11-16, same. When one part is turned over to be glued, its pocket positions mirror (x → −x). The
  first pinned pair did not line up for this reason.

## Bed adhesion

- [O] 2026-11-16/17, same. Thin PETG rings (78 × 97 mm, 2 mm thick) lifted off textured PEI twice with
  `petg-pro-fast-0.4`. The same parts in PLA held.

## PETG

- [O] 2026-11-27, monitor wall mount. **Large PETG first layers on smooth PEI need a thin glue haze, a hot bed
  and a hot-levelled mesh.** Thick glue floated the fill onto the nozzle; raising Z made it worse. The routine is
  in `materials/petg.md`.
- [U] 2026-11-27, same. **Random PETG blobs with dry filament and 0.95 flow point at travels, not flow.** Orca's
  `reduce_infill_retraction` let ~1,500 travels per part cross the infill without retracting or lifting. Now off
  in the PETG profile; not yet confirmed by a print.
