import pytest
import random

import game_context
import player
import cli
from tests import helpers

# test_card_uses.py
# Tests the usage of each card

# black cards

def test_bloodthirsty_spider():
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

def setup_hermit(title):
    """
    Return a game context, element factory, a hunter, shadow
    and neutral from that game, and a card of a given title
    """
    gc, ef = helpers.fresh_gc_ef()
    h = helpers.get_a_hunter(gc)
    s = helpers.get_a_shadow(gc)
    n = helpers.get_a_neutral(gc)
    c = helpers.get_card_by_title(ef, title)
    return (gc, ef, h, s, n, c)

def test_hermit_blackmail():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Blackmail")
    gc.ask_h = helpers.answer_sequence([])

    # Check that

def test_hermit_greed():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Greed")
    gc.ask_h = helpers.answer_sequence([])

    # Check that

def test_hermit_anger():
    
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Anger")
    gc.ask_h = helpers.answer_sequence([])

    # Check that

def test_hermit_slap():
        
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Slap")
    gc.ask_h = helpers.answer_sequence([])

    # Check that

def test_hermit_spell():
    
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Spell")
    gc.ask_h = helpers.answer_sequence([])

    # Check that

def test_hermit_exorcism():
    
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Exorcism")
    gc.ask_h = helpers.answer_sequence([])

    # Check that

def test_hermit_nurturance():
    
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Nurturance")
    gc.ask_h = helpers.answer_sequence([])

    # Check that

def test_hermit_aid():
    
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Aid")
    gc.ask_h = helpers.answer_sequence([])

    # Check that

def test_hermit_fiddle():
    
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Fiddle")
    gc.ask_h = helpers.answer_sequence([])

    # Check that
