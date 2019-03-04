from tests import helpers
import pytest
import area

# test_area.py
# Tests for the Area object

def test_fields():
    
    # test initialization
    a = area.Area(
        name = "area_name",
        desc = "area_desc",
        domain = [9],
        action = lambda: 5,
        resource_id = "r_id"
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
