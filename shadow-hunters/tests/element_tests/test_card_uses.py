import pytest
import random

import game_context
import player
import cli
from tests import helpers

# test_card_uses.py
# Tests the usage of each card
"""
# helper functions to create a rigged game context

def answer_sequence(answers):
    '''create an ask function that will return a specific sequence of answers'''

    def ask_function(x, y, z):
        return 'Amrit'
    return ask_function

def fresh_gc_ef(ask_function = lambda x, y, z: { 'value': random.choice(y['options']) }):
    '''return a fresh game and element factory with the specified ask function'''

    player_names = ['Amrit', 'Max', 'Gia', 'Joanna', 'Vishal']
    players = [player.Player(user_id, socket_id='unused') for user_id in player_names]
    ef = cli.ElementFactory()
    gc = game_context.GameContext(
        players = players,
        characters = ef.CHARACTERS,
        black_cards = ef.BLACK_DECK,
        white_cards = ef.WHITE_DECK,
        green_cards = ef.GREEN_DECK,
        areas = ef.AREAS,
        tell_h = lambda x: 0,
        direct_h = lambda x, sid: 0,
        ask_h = ask_function,
        update_h = lambda x, y: 0
    )
    return (gc, ef)
"""
# black cards

def test_bloodthirsty_spider():
    gc, ef = helpers.fresh_gc_ef()
    assert 1

def test_vampire_bat():
    assert 1

def test_moody_goblin():
    assert 1

def test_butcher_knife():
    assert 1

def test_chainsaw():
    assert 1

def test_broad_axe():
    assert 1

# white cards

def test_holy_robe():
    assert 1

def test_flare_judgement():
    assert 1

def test_first_aid():
    assert 1

def test_holy_water():
    assert 1

# hermit cards

def test_hermit_blackmail():
    assert 1

def test_hermit_greed():
    assert 1

def test_hermit_anger():
    assert 1

def test_hermit_slap():
    assert 1

def test_hermit_spell():
    assert 1

def test_hermit_exorcism():
    assert 1

def test_hermit_nurturance():
    assert 1

def test_hermit_aid():
    assert 1

def test_hermit_fiddle():
    assert 1
