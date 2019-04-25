import helpers
import pytest
import area
import zone

# test_zone.py
# Tests for the Zone object


def test_fields():

    # sample areas
    a1 = area.Area(
        name="area1",
        desc="area desc",
        domain=[8],
        action=lambda: 1,
        resource_id="r_id"
    )
    a2 = area.Area(
        name="area2",
        desc="area desc",
        domain=[9],
        action=lambda: 0,
        resource_id="r_id"
    )

    # test initialization
    areas = [a1, a2]
    z = zone.Zone(areas)

    # test fields
    assert z.areas == areas

    # test dump
    assert z.dump() == [a1.dump(), a2.dump()]

def test_exceptions():
    with pytest.raises(ValueError):
        z1 = zone.Zone(0)

    with pytest.raises(ValueError):
        z2 = zone.Zone([1, 2, 3])

    with pytest.raises(ValueError):
        z3 = zone.Zone([1, 2])
