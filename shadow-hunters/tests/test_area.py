import pytest
import area

# test_area.py
# Tests for the Area object

def test_init():
    a = area.Area(
        name = "Weird Woods",
        desc = "You may either give 2 damage to any player or heal 1 damage of any player.",
        domain = [9],
        action = weird_woods_action,
        resource_id = "weird-woods"
    )
    assert 1
