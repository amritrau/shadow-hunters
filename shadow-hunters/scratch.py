import random
import copy

class Player:
    def __init__(self, username):
        self.username = username
        self.game_context = None
        self.state = 2 #  2 for ALIVE_ANON, 1 for ALIVE_KNOWN, 0 for DEAD
        self.character = None
        self.equipment = []
        self.hp = None
        self.location = None
        self.modifiers = {}

    def setCharacter(self, character):
        self.character = character
        self.hp = self.character.max_hp

    def reveal(self):
        self.modifiers += self.character.modifiers
        self.status = 1

    def takeTurn(self):
        # 1. Roll dice
        # 2. Move to desired location
        # 3. Take action
        # 4. Attack™

        raise NotImplementedError

    def drawCard(self, deck):
        drawn = deck.drawCard()
        if drawn.force_use:
            drawn.use()

    def attack(self, other):
        raise NotImplementedError

    def defend(self, other):
        raise NotImplementedError

    def move(self, location):
        self.location = location


class Character:
    def __init__(self, name, allegiance, max_hp, win_cond, modifiers):
        self.name = name
        self.allegiance = allegiance
        self.max_hp = max_hp
        self.win_cond = win_cond
        self.modifiers = modifiers


class GameContext:
    def __init__(self, players, characters):
        self.players = players
        self.characters = characters
        self.white_cards = Deck(...)
        self.black_cards = Deck(...)
        self.green_cards = Deck(...)
        self.die4 = Die(4)
        self.die6 = Die(6)
        self.modifiers = {}

    def assignRegions():
        raise NotImplementedError

    def assignCharacters():
        n_shadows = floor(len(players) - 1)/2)
        n_hunters = n_shadows
        n_neutrals = len(players) - (n_shadows + n_hunters)

        for player in self.players:
            player.game_context = self
            # TODO assign characters
            # player.character =

        raise NotImplementedError

    def play():
        # Single WHILE loop that runs continuously to play the game
        raise NotImplementedError


class Die:
    def __init__(self, n_sides):
        self.n_sides = n_sides
        self.state = None

    def roll(self):
        self.state = random.randint(1, n_sides)
        return self.state


class Deck:
    def __init__(self, cards):
        self.cards = cards
        self.consumed = []
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def drawCard(self):
        if len(self.cards) > 0:
            drawn = self.cards.pop()
            self.consumed.append(copy.deepcopy(drawn))
            return drawn
        else:
            self.cards, self.consumed = self.consumed, []
            self.shuffle()
            self.drawCard()


class Equipment:
    # Immutable
    def __init__(self, name, description, modifiers):
        self.name = name
        self.description = description
        self.modifiers = modifiers

class Card:
    # Immutable (it might get reshuffled)
    def __init__(self, category, desc, user_mods, target_mods, force_use):
        self.color = color
        self.desc = desc
        self.user_modifiers = user_mods
        self.target_modifiers = target_mods
        self.force_use = force_use

    def use(self, game_context, user, target):
        # 1. Apply the modifiers on the card to the user
        # 2. Apply the modifiers on the card to the target


        raise NotImplementedError
