import pytest
from area import Area
from zone import Zone

# test_zone.py
# Tests for the Zone object


def test_fields():

    # sample areas
    a1 = Area(
        name="area1",
        desc="area desc",
        domain=[8],
        action=lambda: 1,
        resource_id="r_id"
    )
    a2 = Area(
        name="area2",
        desc="area desc",
        domain=[9],
        action=lambda: 0,
        resource_id="r_id"
    )

    # test initialization
    areas = [a1, a2]
    z = Zone(areas)

    # test fields
    assert z.areas == areas

    # test dump
    assert z.dump() == [a1.dump(), a2.dump()]


def test_exceptions():
    with pytest.raises(ValueError):
        z1 = Zone(0)

    with pytest.raises(ValueError):
        z2 = Zone([1, 2, 3])

    with pytest.raises(ValueError):
        z3 = Zone([1, 2])
