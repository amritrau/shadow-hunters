import random

from die import Die
from zone import Zone
# game_context.py
# Implements a GameContext.

class GameContext:
    def __init__(self, players, characters, black_cards, white_cards, green_cards, areas, tell_h, ask_h, update_h, modifiers = dict()):

        # Instantiate gameplay objects
        self.players = players
        self.characters = characters
        self.black_cards = black_cards
        self.white_cards = white_cards
        self.green_cards = green_cards

        # Instantiate message handlers
        self.tell_h = tell_h
        self.ask_h = ask_h
        self.update_h = update_h

        # Assign modifiers
        self.modifiers = modifiers

        # Instantiate dice
        self.die4 = Die(4)
        self.die6 = Die(6)

        # Randomly shuffle areas across zones
        random.shuffle(areas)
        self.zones = [Zone([areas.pop(), areas.pop()]) for i in range(3)]
        for z in self.zones:
            for a in z.areas:
                a.zone = z

        # Randomly assign characters and point game context
        random.shuffle(characters)
        for player in self.players:
            player.setCharacter(characters.pop())
            player.gc = self


    def getLivePlayers(self):
        return [p in self.players if p.state > 0]

    def checkWinConditions(self):
        return [p for p in self.players if p.character.win_cond()]

    def play(self):
        while True:
            for player in self.getLivePlayers():
                    player.takeTurn()
                    winners = self.checkWinConditions()
                    if len(winners):
                        self.tell_h("Players {} won".format(winners))
                        return winners

    def dump(self):
        """
        Return the full GameContext in JSON for debugging
        """
        raise NotImplementedError
        return ""
