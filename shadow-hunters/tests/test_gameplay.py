import pytest
import random

from game_context import gameContext
from player import Player
import cli

# test_gameplay.py
# Tests random walks through the game state for runtime errors

def test_game():
    player_names = ['Amrit', 'Max', 'Gia', 'Joanna', 'Vishal']
    players = [Player(user_id, socket_id='unused') for user_id in player_names]
    for _ in range(100):
        ef = cli.ElementFactory()
        gc = GameContext(
            players = players,
            characters = ef.CHARACTERS,
            black_cards = ef.BLACK_DECK,
            white_cards = ef.WHITE_DECK,
            green_cards = ef.GREEN_DECK,
            areas = ef.AREAS,
            tell_h = lambda x: 0,
            direct_h = lambda x, sid: 0,
            ask_h = lambda x, y, z: random.choice(y['options']),
            update_h = lambda x, y: 0
        )
        winners = gc.play()
        assert winners
    assert 1
