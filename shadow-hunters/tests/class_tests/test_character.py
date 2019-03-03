import pytest
import character

# test_character.py
# Tests for the Character object

def test_init():
    c = character.Character(
        name = "name",
        alleg = 1,
        max_hp = 10,
        win_cond = lambda: 0,
        win_cond_desc = "win desc",
        special = lambda: 0,
        resource_id = "r_id"
    )
    assert 1 
