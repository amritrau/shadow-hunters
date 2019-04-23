import helpers
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
    is_equip = False,
    use = lambda: 0  # placeholder
)

c2 = card.Card(
    title = "Card 2",
    desc = "Another card",
    color = None,  # placeholder
    holder = None,  # placeholder
    is_equip = True,
    use = lambda: 1  # placeholder
)

def test_fields():

    # test initialization
    card_list = [c1, c2]
    d = deck.Deck(cards = card_list)

    # test fields
    assert d.cards == card_list
    assert not d.discard

def test_hashability():
    d1 = deck.Deck(cards = [c1, c2])
    d2 = deck.Deck(cards = [c1, c2])

    # Shuffle `d1` until it is reversed
    desired_order = (c2, c1)
    while tuple(d1.cards) != desired_order:
        d1.shuffle()

    assert(hash(d1) == hash(d1))
    assert(hash(d2) == hash(d2))
    assert(hash(d1) != hash(d2))

    # Shuffle `d2` until it matches `d1`
    while tuple(d2.cards) != tuple(d1.cards):
        d2.shuffle()

    assert(hash(d1) != hash(d2))  # hash of different decks should not be equal

def test_shuffle():
    d = deck.Deck(cards = [c1, c2])
    initial_order = tuple(d.cards)

    def check_shuffled(i):
        d.shuffle()
        return tuple(d.cards) != initial_order

    unmatch_initial = map(check_shuffled, range(100))  # Pr(FN) = 1/(2^100)
    assert(any(unmatch_initial))

def test_drawCard():
    d = deck.Deck(cards = [c1, c2])
    desired_order = (c1, c2)

    # Shuffle until `c2` is at the top of the deck
    while tuple(d.cards) != desired_order:
        d.shuffle()

    original_length = len(d.cards)
    drawn = d.drawCard()

    # Make sure we actually drew `c2` as expected
    assert(hash(drawn) == hash(c2))

    # Check that we decremented the # of cards by 1
    assert(len(d.cards) + 1 == original_length)

    # `c2` is an equipment card, so it doesn't go back in the deck
    # Somewhere above we would append `drawn` to a Player's arsenal
    assert(len(d.discard) == 0)

    drawn = d.drawCard()

    # Make sure we actually drew `c1` as expected
    assert(hash(drawn) == hash(c1))

    # `c1` is not an equipment card so it goes back in the deck
    assert(len(d.discard) == 1)

    # We lost `c2` to some player, so
    assert(len(d.discard) + len(d.cards) == original_length - 1)
