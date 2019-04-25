import helpers
import pytest
import area
import zone

# test_area.py
# Tests for the Area object


def test_fields():

    # test initialization
    a = area.Area(
        name="area_name",
        desc="area_desc",
        domain=[9],
        action=lambda: 5,
        resource_id="r_id"
    )

    # test fields
    assert a.name == "area_name"
    assert a.desc == "area_desc"
    assert len(a.domain) == 1 and a.domain[0] == 9
    assert a.action() == 5
    assert a.resource_id == "r_id"

    # test dump
    dump = a.dump()
    assert dump['name'] == "area_name"
    assert dump['desc'] == "area_desc"
    assert dump['domain'] == "[9]"
    assert str(dump) == str(a)

def test_getAdjacent():

    # Put two areas in a zone
    a = area.Area(
        name="A",
        desc="area_desc",
        domain=[8],
        action=lambda: 5,
        resource_id="a_id"
    )
    b = area.Area(
        name="B",
        desc="area_desc",
        domain=[9],
        action=lambda: 5,
        resource_id="b_id"
    )
    z = zone.Zone([a, b])
    for x in z.areas:
        x.zone = z

    assert a.zone == z
    assert b.zone == z

    # Test adjacency
    assert a.getAdjacent() == b
    assert b.getAdjacent() == a
