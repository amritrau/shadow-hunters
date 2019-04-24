import pytest
import random

import game_context
import player
import elements
import helpers
import constants

# test_gameplay.py
# Tests random walks through the game state for runtime errors


def test_gameplay():
    for _ in range(constants.N_GAMEPLAY_TESTS):
        gc, ef = helpers.fresh_gc_ef()
        gc.play()
    assert 1
