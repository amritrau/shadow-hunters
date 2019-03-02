import pytest
import die

# test_die.py
# Tests for the Die object

def test_init():
    d4 = die.Die(n_sides = 4)
    d6 = die.Die(n_sides = 6)
    assert 1

def test_roll():
    d4 = die.Die(n_sides = 4)
    d6 = die.Die(n_sides = 6)

    d4_rolls = [0, 0, 0, 0]
    d6_rolls = [0, 0, 0, 0, 0, 0]

    # Check that roll is never out of die range
    for _ in range(4000):
        r = d4.roll()
        assert(r >= 1 and r <= 4)
        d4_rolls[r-1] += 1

    for _ in range(6000):
        r = d6.roll()
        assert(r >= 1 and r <= 6)
        d6_rolls[r-1] += 1

    # Check that rolls are reasonably weighted
    assert(all(x > 250 for x in d4_rolls + d6_rolls))

 
