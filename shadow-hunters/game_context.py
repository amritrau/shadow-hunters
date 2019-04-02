import random
import copy

from die import Die
from zone import Zone
import elements

# game_context.py
# Implements a GameContext.

class GameContext:
    def __init__(self, players, characters, black_cards, white_cards, green_cards, areas, tell_h, direct_h, update_h, modifiers = dict()):

        # Instantiate gameplay objects
        self.players = players
        self.turn_order = list(players)
        self.characters = characters
        self.black_cards = black_cards
        self.white_cards = white_cards
        self.green_cards = green_cards

        # Instantiate status
        self.game_over = False

        # Instantiate message handlers
        self.tell_h = tell_h
        self.direct_h = direct_h
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

        # get pool of characters for this game
        all_characters = copy.deepcopy(characters)
        map = elements.TEAMS_MAP[len(players)]
        hunters = [c for c in all_characters if c.alleg == 2]
        shadows = [c for c in all_characters if c.alleg == 0]
        neutrals = [c for c in all_characters if c.alleg == 1]
        random.shuffle(hunters)
        random.shuffle(shadows)
        random.shuffle(neutrals)
        characters_in_game = ([shadows.pop() for _ in range(map[0])] +
                              [neutrals.pop() for _ in range(map[1])] +
                              [hunters.pop() for _ in range(map[2])])

        # Randomly assign characters and point game context
        random.shuffle(characters_in_game)
        for player in self.players:
            player.setCharacter(characters_in_game.pop())
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
                    self.tell_h("{} ({}: {}) won! {}".format(
                        w.user_id,
                        elements.ALLEGIANCE_MAP[w.character.alleg],
                        w.character.name,
                        w.character.win_cond_desc
                    ))
            return winners

    def play(self):
        turn = random.randint(0, len(self.turn_order) - 1)
        while True:
            current_player = self.turn_order[turn]
            if current_player.state:
                current_player.takeTurn()
            winners = self.checkWinConditions()
            if winners:
                return winners
            turn += 1
            if turn >= len(self.turn_order):
                turn = 0
                self.turn_order = list(self.players)

    def dump(self):
        public_zones = [z.dump() for z in self.zones]
        private_players = {p.socket_id: p.dump() for p in self.players}
        public_players = copy.deepcopy(private_players)

        # Hide character information if player hasn't revealed themselves
        for k,v in public_players.items():
            if public_players[k]['state'] == 2:
                public_players[k]['character'] = {}

        # Collect the public states
        public_state = {
            'zones': public_zones,
            'players': public_players,
            'characters': [c.dump() for c in self.characters]
        }
        private_state = private_players


        return public_state, private_state
