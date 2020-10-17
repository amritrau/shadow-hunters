import random
import copy

from die import Die
from zone import Zone
import elements
import constants

# game_context.py
# Implements a GameContext.


class GameContext:
    def __init__(self, players, characters, black_cards, white_cards,
                 green_cards, areas, ask_h, tell_h, show_h, update_h,
                 modifiers=dict()):

        # Instantiate gameplay objects
        self.players = players
        self.turn_order = copy.copy(players)
        self.round_count = 0

        # Assign "local delexicalizations" for each player.
        # Reason: This allows a game-playing agent to parse data dumps about
        # its opponents regardless of what their particular screen names are.
        #
        # Implementation: Each player has `delexicalizations`, which is a
        # dictionary that maps user_id => delexicalization. Player p's
        # delexicalization dictionary follows the turn order starting with p,
        # so that p.delexicalizations[p.user_id] = 0. The player whose turn is
        # next, q, is delexicalized from p's view as 1:
        #  > p.delexicalizations[q.user_id] = 1
        # ... and so on.
        for p in self.players:
            n = self.turn_order.index(p) - 1
            d = self.turn_order[-n:] + self.turn_order[:-n]
            inv = dict(enumerate(d)).items()
            p.delexicalizations = {v.user_id: k for k, v in inv}

        # Instantiate characters
        self.characters = characters
        if len(self.players) <= 6:
            self.characters = [
                ch for ch in self.characters if ch.resource_id != "bob2"]
        else:
            self.characters = [
                ch for ch in self.characters if ch.resource_id != "bob1"]
        self.characters.sort(key=lambda x: -x.max_damage)

        # Instantiate cards
        self.black_cards = black_cards
        self.white_cards = white_cards
        self.green_cards = green_cards

        # Instantiate status
        self.game_over = False

        # Instantiate message handlers
        self.ask_h = ask_h
        self.tell_h = tell_h
        self.show_h = show_h
        self.update_h = update_h

        # Instantiate answer bin
        self.answer_bin = {
            'answered': False,
            'sid': '',
            'data': {}
        }

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

        # Figure out how many of each allegiance there has to be
        counts_dict = {
            4: (2, 0, 2),
            5: (2, 1, 2),
            6: (2, 2, 2),
            7: (2, 3, 2),
            8: (3, 2, 3)
        }

        # Randomly assign characters and point game context
        character_q = copy.deepcopy(self.characters)
        random.shuffle(character_q)
        queue = []
        while character_q:
            ch = character_q.pop()
            already_in = len([c for c in queue if c.alleg == ch.alleg])
            if (already_in < counts_dict[len(self.players)][ch.alleg]):
                queue.append(ch)

        assert(len(queue) == len(self.players))

        for player in self.players:
            player.setCharacter(queue.pop())
            player.gc = self

    def getLivePlayers(self, filter_fn=(lambda x: True)):
        res = filter(filter_fn, [p for p in self.players if p.state > 0])
        return list(res)

    def getDeadPlayers(self, filter_fn=(lambda x: True)):
        res = filter(filter_fn, [p for p in self.players if p.state < 1])
        return list(res)

    def getPlayersAt(self, location_name):
        live = self.getLivePlayers()
        live_loc = [p for p in live if p.location]
        return [p for p in live_loc if p.location.name == location_name]

    def getAreas(self):
        areas = []
        for z in self.zones:
            for a in z.areas:
                areas.append(a.name)

        return areas

    def getAreaFromRoll(self, roll_result):
        # Get area from roll
        destination_Area = None
        for z in self.zones:
            for a in z.areas:
                if roll_result in a.domain:
                    destination_Area = a

        return destination_Area

    def _checkWinConditions(self):
        return [p for p in self.players if p.character.win_cond(self, p)]

    def checkWinConditions(self, tell=True):
        winners = self._checkWinConditions()
        if len(winners):
            self.game_over = True
            winners = self._checkWinConditions()  # Hack to collect Allie
            if tell:
                display_data = {'type': 'win', 'winners': [
                    p.dump() for p in winners]}
                self.show_h(display_data)
                for w in winners:
                    self.tell_h("{} ({}: {}) won! {}", [
                        w.user_id,
                        constants.ALLEGIANCE_MAP[w.character.alleg],
                        w.character.name,
                        w.character.win_cond_desc
                    ])
            return winners

    def play(self):
        turn = random.randint(0, len(self.turn_order) - 1)
        while True:
            current_player = self.turn_order[turn]
            if current_player.state:
                current_player.takeTurn()
            winners = self.checkWinConditions()
            if winners:
                break
            turn += 1
            if turn >= len(self.turn_order):
                turn = 0
                self.round_count += 1
                self.turn_order = list(self.players)

    def dump(self):
        # Note that public_players and private_state are no longer keyed by
        # socket_ids
        public_zones = [z.dump() for z in self.zones]
        private_players = [p.dump() for p in self.players]
        public_players = copy.deepcopy(private_players)

        # Hide character information if player hasn't revealed themselves
        for p in public_players:
            if p['state'] == 2:
                p['character'] = {}

        # Collect the public states
        public_state = {
            'zones': public_zones,
            'players': public_players,
            'characters': [c.dump() for c in self.characters]
        }
        private_state = private_players

        return public_state, private_state
