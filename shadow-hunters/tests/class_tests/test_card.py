import pytest
import card

# test_card.py
# Tests for the Card object

def test_init():
    c = card.Card(
        title = "a card",
        desc = "card desc",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = False,
        use = lambda: 0
    )
    assert 1
