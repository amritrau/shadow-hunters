import pytest
import random

import game_context
import player
import elements
import helpers

# test_gameplay.py
# Tests random walks through the game state for runtime errors


def test_gameplay():
    for _ in range(1000):
        gc, ef = helpers.fresh_gc_ef()
        gc.play()
    assert 1
