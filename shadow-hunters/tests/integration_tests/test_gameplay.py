import pytest
import random

import game_context
import player
import cli
from tests import helpers

# test_gameplay.py
# Tests random walks through the game state for runtime errors

def test_gameplay():
    for _ in range(10000):
        gc, ef = helpers.fresh_gc_ef()
        winners = gc.play()
        print("GAME OVER - Winners: ", [winner.user_id for winner in winners])
        assert winners
    assert 1
