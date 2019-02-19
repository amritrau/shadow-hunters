import pytest
import card, deck

# test_deck.py
# Tests for the Deck object

# Initialize some global objects
c1 = card.Card(
    title = "Card 1",
    desc = "Some card",
    color = None, # placeholder
    holder = None,  # placeholder
    is_equip = True,
    force_use = False,
    use = lambda: 0  # placeholder
)
c2 = card.Card(
    title = "Card 2",
    desc = "Another card",
    color = None,  # placeholder
    holder = None,  # placeholder
    is_equip = True,
    force_use = False,
    use = lambda: 1  # placeholder
)

def test_init():
    d = deck.Deck(cards = [c1, c2])
    assert 1

def test_shuffle():
    d = deck.Deck(cards = [c1, c2])
    initial_order = tuple(d.cards)

    def check_shuffled(i):
        d.shuffle()
        return tuple(d.cards) != initial_order

    unmatch_initial = map(check_shuffled, range(100))
    assert(any(unmatch_initial))
