import types

import pytest

from workshop.measure import Unmeasured, dims, mm


def test_mm_passes_values_and_refuses_none():
    assert mm(3.4, "HOLE") == 3.4
    with pytest.raises(Unmeasured, match="HOLE has not been measured yet. calipers"):
        mm(None, "HOLE", "calipers")


def test_dims_reads_a_module():
    m = types.SimpleNamespace(A=1.5, B=None)
    dim = dims(m)
    assert dim("A") == 1.5
    with pytest.raises(Unmeasured, match="B"):
        dim("B")
