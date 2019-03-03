import pytest
import area, zone

# test_zone.py
# Tests for the Zone object

def test_init():
    a1 = area.Area(
        name = "area1",
        desc = "area desc",
        domain = [8],
        action = lambda: 1,
        resource_id = "r_id"
    )
    a2 = area.Area(
        name = "area2",
        desc = "area desc",
        domain = [9],
        action = lambda: 0,
        resource_id = "r_id"
    )
    z = zone.Zone([a1, a2])
    assert 1
