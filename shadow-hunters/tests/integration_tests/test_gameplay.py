import pytest
import random

from utils import make_hash_sha256
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


def test_regression():
    """Test that a refactor or reorganization doesn't affect intermediate or
    final game states when compared to a stable branch.

    Note that `correct_hash` must be updated from a stable branch in the
    following scenarios:
     - game logic changes
     - representation of public/private states change (including order)
     - constants.N_GAMEPLAY_TESTS changes

    This test is somewhat slow to run because hashing is slow.
    """
    random.seed(C.TEST_RANDOM_SEED)
    game_hashes = ""
    for _ in range(C.N_GAMEPLAY_TESTS):
        for n in range(4, 9):
            gc, ef = fresh_gc_ef(n)
            game_hashes += gc.play(debug=True)

    correct_hash = 'YYRGN3eJZeq3jYVYCoqHAPOVR6YF720QSk5ZY8G94Rc='
    found_hash = make_hash_sha256(game_hashes)
    assert correct_hash == found_hash
