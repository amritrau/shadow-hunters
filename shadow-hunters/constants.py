from enum import Enum


# Enum for character allegiances
class Alleg(Enum):
    Shadow = 0
    Neutral = 1
    Hunter = 2


# Enum for card type
class CardType(Enum):
    White = 0
    Black = 1
    Hermit = 2


# Enum for player state
class PlayerState(Enum):
    Dead = 0
    Revealed = 1
    Hidden = 2


# Enum for text colors
TEXT_COLORS = {
    'server': 'rgb(200,200,200)',
    'number': 'rgb(153,204,255)',
    'White': 'rgb(255,255,255)',
    'Black': 'rgb(75,75,75)',
    'Green': 'rgb(143,194,0)',
    'shadow': 'rgb(128,0,0)',
    'neutral': 'rgb(255,255,153)',
    'hunter': 'rgb(51,51,255)',
    'Weird Woods': 'rgb(102,153,153)',
    'Church': 'rgb(255,255,255)',
    'Cemetery': 'rgb(75,75,75)',
    'Erstwhile Altar': 'rgb(204,68,0)',
    'Hermit\'s Cabin': 'rgb(143,194,0)',
    'Underworld Gate': 'rgb(150,0,150)'
}

# Number of gameplay tests to run
N_GAMEPLAY_TESTS = 100  # = 500 games
N_REGRESSION_TESTS = 20  # = 100 games
N_ELEMENT_TESTS = 100

# Random seed for testing
TEST_RANDOM_SEED = 124
