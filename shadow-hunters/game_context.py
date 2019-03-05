import random
import copy

from die import Die
from zone import Zone
import elements

# game_context.py
# Implements a GameContext.

class GameContext:
    def __init__(self, players, characters, black_cards, white_cards, green_cards, areas, tell_h, direct_h, ask_h, update_h, modifiers = dict()):

        # Instantiate gameplay objects
        self.players = players
        self.characters = characters
        self.black_cards = black_cards
        self.white_cards = white_cards
        self.green_cards = green_cards

        # Instantiate status
        self.game_over = False

        # Instantiate message handlers
        self.tell_h = tell_h
        self.direct_h = direct_h
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
        return [p for p in self.players if p.state > 0]

    def getDeadPlayers(self):
        return [p for p in self.players if p.state == 0]

    def _checkWinConditions(self):
        return [p for p in self.players if p.character.win_cond(self, p)]

    def checkWinConditions(self, tell = True):
        winners = self._checkWinConditions()
        if len(winners):
            self.game_over = True
            winners = self._checkWinConditions()  # Hack to collect Allie
            if tell:
                for w in winners:
                    self.tell_h("{} ({}: {}) won! {}".format(w.user_id, elements.ALLEGIANCE_MAP[w.character.alleg], w.character.name, w.character.win_cond_desc))
            return winners


    def play(self):
        for z in range(len(self.zones)):
            self.tell_h("Zone {} contains: {}.".format(z+1, ', '.join([a.name for a in self.zones[z].areas])))
        for p in self.players:
            self.direct_h("You ({}) are {} ({}).".format(p.user_id, p.character.name, elements.ALLEGIANCE_MAP[p.character.alleg]), p.socket_id)
        while True:
            for player in self.getLivePlayers():
                    player.takeTurn()
                    winners = self.checkWinConditions()
                    if winners:
                        return winners

    def dump(self):
        public_zones = [z.dump() for z in self.zones]
        private_players = {p.socket_id: p.dump() for p in self.players}
        public_players = copy.deepcopy(private_players)

        # Hide character information if player hasn't revealed themselves
        for k,v in public_players.items():
            if public_players[k]['state'] == 2:
                public_players[k]['character'] = {}

        public_state = {
            'zones': public_zones,
            'players': public_players
        }
        private_state = private_players


        return public_state, private_state
