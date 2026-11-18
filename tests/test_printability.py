import pytest

pytest.importorskip("build123d")
pytest.importorskip("shapely")

from workshop.cad import geometry  # noqa: E402
from workshop.cad.export import export  # noqa: E402
from workshop.cad.printability import footprint, layers, load, mesh_check  # noqa: E402


def test_block_is_printable(tmp_path):
    stl = export("block", geometry.box(0, 20, 0, 10, 0, 5), tmp_path)
    assert mesh_check(stl)["connected_components"] == 1
    summary, rows = layers(stl)
    assert len(rows) == 25
    assert summary["max_area_outside_45deg_layer_envelope_mm2"] < 1e-6
    assert footprint(load(stl), 2.5).area == pytest.approx(200, abs=1e-3)


def test_shelf_outside_the_cone_is_reported(tmp_path):
    # A 10 mm flat shelf 4 mm up: the layer above the step lies outside the 45° cone.
    part = geometry.box(0, 10, 0, 10, 0, 6) + geometry.box(10, 20, 0, 10, 4, 6)
    stl = export("shelf", part, tmp_path)
    summary, _ = layers(stl)
    assert summary["max_area_outside_45deg_layer_envelope_mm2"] > 50
    assert summary["max_downward_surface_angle_from_vertical_deg"] == pytest.approx(90, abs=0.1)


def test_floating_part_fails_mesh_check(tmp_path):
    stl = export("floating", geometry.box(0, 10, 0, 10, 1, 5), tmp_path)
    with pytest.raises(AssertionError):
        mesh_check(stl)
