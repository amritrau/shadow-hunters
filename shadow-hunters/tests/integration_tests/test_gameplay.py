import pytest

from helpers import fresh_gc_ef
import constants as C

# test_gameplay.py
# Tests random walks through the game state for runtime errors

def test_gameplay():
    for _ in range(C.N_GAMEPLAY_TESTS):
        for n in range(4, 9):
            gc, ef = fresh_gc_ef(n)
            gc.play()
    assert 1
