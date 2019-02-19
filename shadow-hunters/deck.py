import random
import copy

from card import Card
# deck.py
# Implements the Deck object.

class Deck:
    """
    A Deck of Card objects. Implements shuffling and re-shuffling of a discard
    pile.
    """
    def __init__(self, cards):
        # Make sure a list is passed to cards
        if not isinstance(cards, list):
            raise ValueError("cards must be a list.")

        self.cards = cards  # note that cards are ordered [bottom, ... top]

        # Make sure every card in self.cards is a Card object
        for c in self.cards:
            if not isinstance(c, Card):
                raise ValueError("One or more cards is not a Card object.")

        self.discard = []
        self.shuffle()

    def shuffle(self):
        """
        Randomly shuffle the active cards.
        """
        random.shuffle(self.cards)

    def drawCard(self):
        """
        Draw a card from the top of the deck.
        """
        if len(self.cards) > 0:
            drawn = self.cards.pop()

            # Discard the card IFF it is not an equipment card
            if not drawn.is_equipment:
                self.discard.append(copy.deepcopy(drawn))

            return drawn
        else:
            self.cards, self.discard = self.discard, []
            self.shuffle()
            return self.drawCard()
