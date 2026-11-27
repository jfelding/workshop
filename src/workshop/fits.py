"""Measured fit allowances: how big to model a hole so the printed one fits.

Printed holes come out small by an amount that belongs to one machine, material and nozzle
(a *process*). This module holds what has been measured for each process and turns a
mating part's size into the size to model. A process nobody has measured raises
:class:`Uncharacterised`, for the same reason :func:`workshop.measure.mm` refuses unmeasured
dimensions: a guess here costs a print. The evidence behind every number is in
`materials/fits.md`; change a number there and here together, with the date and the part
that showed it.

    from workshop.fits import hole_for, nut_pocket
    bore = hole_for(6.0, 'running')          # Ø6 pin turning in PLA on the Neptune: 6.5
    af, depth = nut_pocket(5.2, 2.1, 'press')  # thin M3 nut: 5.35 AF, 2.4 deep
"""
from dataclasses import dataclass, field


class Uncharacterised(KeyError):
    """No measured fits for this machine, material and nozzle, or not for this fit."""

    def __str__(self):
        return self.args[0]


@dataclass(frozen=True)
class Fit:
    """Printed diametral clearance (mm, negative = interference) and how sure we are of it."""
    clearance: float
    evidence: str          # 'measured', 'in use' (built, not measured) or 'untested'
    source: str


@dataclass(frozen=True)
class Process:
    machine: str
    material: str
    nozzle: float
    #: Small vertical holes print this much under their modelled diameter.
    hole_shrink: float
    fits: dict = field(default_factory=dict)
    #: Hex pockets: added across flats and to depth, by kind of fit.
    nut_pocket: dict = field(default_factory=dict)
    #: Pilot hole for a self-tapping screw, by thread.
    self_tap: dict = field(default_factory=dict)
    #: Between two printed parts: a sliding fit, and a part dropped into a pocket.
    printed_slide: float | None = None
    printed_pocket: float | None = None
    #: A flat rigid sheet (metal, glass) dropped into a printed seat: total clearance along each side.
    sheet_seat: Fit | None = None
    #: Gaps narrower than this between printed walls do not survive (the printer resolves ~0.4).
    min_gap: float | None = None
    elephant_foot: float | None = None


PROCESSES = {
    ('neptune-3-pro', 'pla', 0.4): Process(
        machine='neptune-3-pro', material='pla', nozzle=0.4,
        hole_shrink=0.2,
        fits={
            'press': Fit(-0.05, 'untested', 'LED caps v3 bore Ø6.0 on a Ø5.85 flange, 2026-10-29'),
            'slip': Fit(0.05, 'untested', 'LED caps v3 bore Ø6.1 on a Ø5.85 flange, 2026-10-29'),
            'running': Fit(0.3, 'measured', 'head frame v2 pivot Ø6.5 for a Ø6 pin, 2026-10-09'),
        },
        nut_pocket={
            'press': (0.15, 0.3, 'measured', 'thin M3 nut 5.2 AF × 2.1 in 5.35 × 2.4, carrier v2, 2026-10-13'),
            'clearance': (0.3, 0.4, 'in use', 'earlier builds; never failed, never measured'),
        },
        self_tap={'M3': 2.5},
        printed_slide=0.5, printed_pocket=0.3,
        sheet_seat=Fit(0.3, 'untested', 'sheet holders, 2026-10-13: 0.2 fit a 70 × 20 × 1 mm sheet on a '
                       'flat coupon but needed filing on the full holders; 0.3 not yet printed'),
        min_gap=0.8, elephant_foot=0.15,
    ),
    ('neptune-3-pro', 'petg', 0.4): Process(
        machine='neptune-3-pro', material='petg', nozzle=0.4,
        hole_shrink=0.15,       # Ø5.5 printed ~5.35 (monitor-mount fit slice, 2026-11-27)
        nut_pocket={
            # Side-entry slots: the nut slides in sideways under a bridged ceiling, and the bridge sags.
            'slot_tight': (0.1, 0.4, 'measured', 'monitor-mount coupon, 2026-11-27: M4 nut 7.0 AF × 3.2 slid '
                           'into a 7.1 × 3.6 slot with effort; the +0.2 to +0.4 AF slots sagged more and refused it'),
            'slot': (0.3, 1.0, 'untested', 'chosen from slot_tight: +0.6 mm of height for ceiling sag, '
                     '+0.2 AF of margin; a loose nut costs nothing, the screw pulls it home'),
        },
    ),
    ('neptune-3-pro', 'pla', 0.2): Process(
        machine='neptune-3-pro', material='pla', nozzle=0.2,
        hole_shrink=None, elephant_foot=0.10,
    ),
}

#: ISO 273 medium clearance holes. Model them at this size; a tight one is reamed.
CLEARANCE = {'M2': 2.4, 'M2.5': 2.9, 'M3': 3.4, 'M4': 4.5, 'M5': 5.5, 'M6': 6.6, 'M8': 9.0}

DEFAULT = ('neptune-3-pro', 'pla', 0.4)


def process(machine=DEFAULT[0], material=DEFAULT[1], nozzle=DEFAULT[2]):
    """The measured process, or :class:`Uncharacterised` saying what to print first."""
    try:
        return PROCESSES[(machine, material, nozzle)]
    except KeyError:
        raise Uncharacterised(
            f'no fits measured for {material} on {machine} with a {nozzle} mm nozzle: print a cheap real '
            f'part carrying the fit, measure it, and add the numbers to materials/fits.md and fits.py'
        ) from None


def _need(value, what, p):
    if value is None:
        raise Uncharacterised(f'{what} not measured for {p.material} on {p.machine}, {p.nozzle} mm nozzle')
    return value


def hole_for(shaft, fit='slip', p=None):
    """Diameter to model a vertical hole so it prints with `fit` on a `shaft` (mm).

    Horizontal holes print differently (and want a teardrop): this is for holes along Z.
    """
    p = p or process()
    shrink = _need(p.hole_shrink, 'hole shrink', p)
    if fit not in p.fits:
        raise Uncharacterised(f"no '{fit}' fit for {p.material} on {p.machine}; known: {', '.join(p.fits)}")
    return round(shaft + p.fits[fit].clearance + shrink, 3)


def nut_pocket(across_flats, thickness, fit='clearance', p=None):
    """(across flats, depth) to model a hex pocket for a nut of this size."""
    p = p or process()
    if fit not in p.nut_pocket:
        raise Uncharacterised(f"no '{fit}' nut pocket for {p.material} on {p.machine}, {p.nozzle} mm nozzle")
    d_af, d_depth, _, _ = p.nut_pocket[fit]
    return round(across_flats + d_af, 3), round(thickness + d_depth, 3)


def pilot(thread, p=None):
    """Pilot hole for a self-tapping screw of `thread` (e.g. 'M3') into this process's plastic."""
    p = p or process()
    if thread not in p.self_tap:
        raise Uncharacterised(f'no self-tapping pilot for {thread} in {p.material} on {p.machine}')
    return p.self_tap[thread]


def sheet_seat(length, width, p=None):
    """(length, width) to model a printed seat that a flat sheet of this size drops into."""
    p = p or process()
    c = _need(p.sheet_seat, 'sheet seat', p).clearance
    return round(length + c, 3), round(width + c, 3)


def clearance(thread):
    """ISO 273 medium clearance hole for `thread`."""
    return CLEARANCE[thread]
