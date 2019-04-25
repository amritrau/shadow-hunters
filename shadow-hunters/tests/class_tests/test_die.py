import helpers
import pytest
import die

# test_die.py
# Tests for the Die object


def test_fields():

    # test initialization
    d4 = die.Die(n_sides=4)

    # test fields
    assert d4.n_sides == 4
    assert d4.state is None
    r = d4.roll()
    assert d4.state == r


def test_roll():

    # Initialize
    d4 = die.Die(n_sides=4)
    d6 = die.Die(n_sides=6)

    d4_rolls = [0, 0, 0, 0]
    d6_rolls = [0, 0, 0, 0, 0, 0]

    # Check that roll is never out of die range
    for _ in range(4000):
        r = d4.roll()
        assert(r >= 1 and r <= 4)
        d4_rolls[r - 1] += 1

    for _ in range(6000):
        r = d6.roll()
        assert(r >= 1 and r <= 6)
        d6_rolls[r - 1] += 1

    # Check that rolls are reasonably weighted
    assert(all(x > 250 for x in d4_rolls + d6_rolls))


def test_exceptions():
    with pytest.raises(ValueError):
        d = die.Die(0)
