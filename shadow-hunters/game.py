import random

class Player:
    def __init__(self, username):
        self.username = username
        self.status = 1 #  1 for ALIVE, 2 for DEAD
        self.equipment = []
        self.location = None


class Character:
    def __init__(self, name, allegiance, max_hp, win_cond):
        self.name = name
        self.allegiance = allegiance
        self.max_hp = max_hp
        self.win_cond = win_cond


class GameContext:
    def __init__(self, players, playable_characters):
        self.players = players
        self.playable_characters = playable_characters
        self.white_cards = Deck(...)
        self.black_cards = Deck(...)
        self.green_cards = Deck(...)


class Dice:
    def __init__(self, n_sides):
        self.n_sides = n_sides

    def roll(self):
        return random.randint(1, n_sides)


class Deck:
    def __init__(self, cards):
        self.cards = cards
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def drawCard(self):
        drawn = self.cards.pop()

        return drawn


class Equipment:
    def __init__(self, name, information):
        self.name = name
        self.information = information

class Card:
    def __init__(self, category, description, information):
        self.category = category
        self.description = description
        self.information = information

    def apply(self):
        # Apply the information on the card to the GameContext
        raise NotImplementedError
