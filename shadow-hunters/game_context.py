import random

from die import Die
from zone import Zone
# game_context.py
# Implements a GameContext.

class GameContext:
    def __init__(self, players, characters, black_cards, white_cards, green_cards, areas, modifiers = dict()):
        self.players = players
        self.black_cards = black_cards
        self.white_cards = white_cards
        self.green_cards = green_cards
        self.modifiers = modifiers

        # Instantiate dice
        self.die4 = Die(4)
        self.die6 = Die(6)

        # Randomly shuffle areas across zones
        random.shuffle(areas)
        self.zones = [zone.Zone([areas.pop(), areas.pop()] for i in range(3)]

        # Randomly assign characters
        random.shuffle(characters)
        for player in self.players:
            player.character = characters.pop()


    def checkWinConditions(self):
        return [p for p in players if p.win_cond()]

    def play(self):
        """
        Game loop
        """

        raise NotImplementedError

        while True:
            # TODO Game action here
            for player in self.players:
                if player.state > 0:  # Alive
                    player.takeTurn()

            winners = self.checkWinConditions()
            if winners:
                return winners

    def dump(self):
        """
        Return the full GameContext in JSON for debugging
        """
        raise NotImplementedError
        return ""
