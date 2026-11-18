import pytest

from workshop.fits import Uncharacterised, clearance, hole_for, nut_pocket, pilot, process


def test_numbers_match_the_parts_that_proved_them():
    assert hole_for(6.0, "running") == 6.5      # head frame v2 pivot
    assert hole_for(5.85, "slip") == 6.1        # LED caps v3
    assert hole_for(5.85, "press") == 6.0
    assert nut_pocket(5.2, 2.1, "press") == (5.35, 2.4)   # thin M3 nut, carrier v2
    assert pilot("M3") == 2.5
    assert clearance("M3") == 3.4


def test_unmeasured_process_refuses():
    with pytest.raises(Uncharacterised, match="petg"):
        process(material="petg")
    with pytest.raises(Uncharacterised, match="hole shrink"):
        hole_for(3.0, "slip", process(nozzle=0.2))
    with pytest.raises(Uncharacterised, match="interference"):
        hole_for(3.0, "interference")


def test_sheet_seat_adds_total_clearance():
    from workshop.fits import sheet_seat
    assert sheet_seat(70, 20) == (70.3, 20.3)
