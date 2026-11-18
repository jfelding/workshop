import math

import pytest

pytest.importorskip("build123d")

from workshop.cad import checks, geometry  # noqa: E402
from workshop.cad.export import export  # noqa: E402


def test_box_extents_and_overlap():
    a = geometry.box(0, 10, 0, 10, 0, 10)
    b = geometry.box(5, 15, 0, 10, 0, 10)
    c = geometry.box(10, 20, 0, 10, 0, 10)        # touches a face only
    assert checks.overlap(a, b) == pytest.approx(500)
    assert checks.overlap(a, c) == 0
    checks.assert_clear([("touching", a, c)])
    with pytest.raises(AssertionError, match="overlapping 500"):
        checks.assert_clear([("overlapping", a, b)])


def test_probe_measures_wall():
    plate = geometry.box(0, 20, 0, 20, 0, 5) - geometry.cylinder(3, 5, "z", (10, 10, 2.5))
    assert checks.probe(plate, (10, 10, 2.5), (30, 10, 2.5)) == pytest.approx(7, abs=1e-6)


def test_teardrop_is_round_below_and_pointed_above():
    d = 6.0
    t = geometry.teardrop(d, 10, "x", (0, 0, 0), up="z")
    bb = t.bounding_box()
    assert bb.min.Z == pytest.approx(-3)
    assert bb.max.Z == pytest.approx(d / math.sqrt(2), abs=1e-6)
    assert bb.max.Y == pytest.approx(3, abs=1e-6)          # never wider than the hole
    # A Z-up block with this hole cut has no flat ceiling to bridge.
    block = geometry.box(-5, 5, -10, 10, -8, 10) - t
    assert checks.overhangs(block)["flat_ceilings_mm2"] < 1e-6
    with pytest.raises(ValueError):
        geometry.teardrop(d, 10, "z", (0, 0, 0), up="z")


def test_revolution_envelope_contains_an_off_axis_block():
    arm = geometry.box(10, 20, -2, 2, 0, 4)
    env = checks.revolution_envelope(arm, "z", (0, 0, 0), slab=2.0)
    r = max(e[1][2] for e in env)
    assert r == pytest.approx(math.hypot(20, 2), rel=1e-3)
    assert checks.sweep_angles(0, 10, 3) == pytest.approx([0, 2.5, 5, 7.5, 10])


def test_bed_and_export(tmp_path):
    p = geometry.box(0, 200, 0, 10, 0, 5)
    assert checks.fits_bed(p, (220, 220, 270))
    assert not checks.fits_bed(p, (150, 150, 270))
    stl = export("bar", p, tmp_path)
    assert stl.exists() and (tmp_path / "bar.step").exists() and (tmp_path / "bar.png").exists()
    with pytest.raises(ValueError, match="one valid solid"):
        export("two", geometry.box(0, 1, 0, 1, 0, 1) + geometry.box(5, 6, 0, 1, 0, 1), tmp_path)
