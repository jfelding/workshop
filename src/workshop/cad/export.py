"""Write printable parts as STL and STEP, refusing anything that is not one valid solid.

A boolean that silently leaves two solids, or an invalid shell, slices into something odd and
is found only at the printer. Exports go to ``out`` (by convention the project's
`exports/`). Each export also writes ``name.png``, a 3D view titled with the part's name and
size: commit it and show it in the README, so a person can tell which file is which
(`ws-check-pictures` enforces this).
"""
from pathlib import Path

from build123d import Compound, export_step, export_stl

from .preview import preview


def export(name, part, out, **stl):
    """One part in print orientation -> ``out/name.{stl,step,png}``. Returns the STL path.

    ``stl`` passes ``tolerance`` / ``angular_tolerance`` to build123d's STL tessellation.
    """
    solids = part.solids()
    if len(solids) != 1 or not part.is_valid:
        raise ValueError(f'{name}: expected one valid solid, got {len(solids)} (valid={part.is_valid})')
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    export_stl(part, out/f'{name}.stl', **stl)
    export_step(part, out/f'{name}.step')
    b = part.bounding_box()
    print(f'{name}: {b.size.X:.1f} × {b.size.Y:.1f} × {b.size.Z:.1f} mm, {part.volume/1000:.1f} cm³ → {out/name}.stl')
    preview(out/f'{name}.stl')
    return out/f'{name}.stl'


def export_many(name, solids, out, **stl):
    """Several separate solids in one print job; each must already be valid."""
    if not all(s.is_valid for s in solids):
        raise ValueError(f'{name}: invalid solid in the job')
    comp = Compound(children=solids)
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    export_stl(comp, out/f'{name}.stl', **stl)
    export_step(comp, out/f'{name}.step')
    b = comp.bounding_box()
    print(f'{name}: {len(solids)} solids, {b.size.X:.0f} × {b.size.Y:.0f} × {b.size.Z:.1f} mm → {out/name}.stl')
    preview(out/f'{name}.stl')
    return out/f'{name}.stl'
