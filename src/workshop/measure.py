"""The one rule of CAD in this workshop: a part never builds on a dimension nobody measured.

Each project keeps its physical dimensions in one module (by convention `cad/measurements.py`).
A dimension that has not been measured is ``None`` there, never a plausible guess, and parts
read every value through :func:`mm`, which refuses to build and names the missing value.
A part that will not build costs two seconds; a part built on an invented number costs a
print. See `methods/cad-in-code.md`.

    from workshop.measure import mm
    import measurements as m
    bore = mm(m.SHAFT_DIAMETER, "SHAFT_DIAMETER", "calipers, three places")
"""


class Unmeasured(Exception):
    """Raised when a model asks for a dimension nobody has measured yet."""


#: Where a project lists what still has to be measured, quoted in the error.
TO_MEASURE = "inventory/to-measure.md"


def mm(value, name, hint=""):
    """Return ``value``, or stop the build and say which measurement is missing."""
    if value is None:
        msg = f"{name} has not been measured yet."
        if hint:
            msg += f" {hint}"
        msg += f" See {TO_MEASURE}."
        raise Unmeasured(msg)
    return value


def dims(module):
    """``dim(name)`` bound to a measurements module: ``dim = dims(m); dim('MOTOR_FRAME')``."""
    def dim(name, hint=""):
        return mm(getattr(module, name), name, hint)
    return dim
