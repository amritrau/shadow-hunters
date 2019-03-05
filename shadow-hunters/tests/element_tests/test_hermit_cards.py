import pytest
import random

import game_context
import player
from tests import helpers

# test_hermit_cards.py
# Tests the usage of each hermit card

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
    gc.ask_h = helpers.answer_sequence([
        h.user_id, 'Receive 1 damage',                   # test for hunter
        s.user_id, 'Do nothing',                         # test for shadow
        n.user_id, 'Receive 1 damage',                   # test for neutral
        h.user_id, 'Give an equipment card', 'Holy Robe' # test for giving equipment
    ])

    # Check that hunters take 1 damage
    init_hp = h.hp
    c.use({ 'self': s })
    assert h.hp == init_hp + 1

    # Check that shadows do nothing
    init_hp = s.hp
    c.use({ 'self': h })
    assert s.hp == init_hp

    # Check that neutrals take 1 damage
    init_hp = n.hp
    c.use({ 'self': h })
    assert n.hp == init_hp + 1

    # Check that giving equipment works
    eq = helpers.get_card_by_title(ef, 'Holy Robe')
    h.equipment.append(eq)
    init_hp = h.hp
    c.use({ 'self': s })
    assert h.hp == init_hp
    assert not h.equipment
    assert s.equipment == [eq]

def test_hermit_greed():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Greed")
    gc.ask_h = helpers.answer_sequence([
        h.user_id, 'Do nothing',                         # test for hunter
        s.user_id, 'Receive 1 damage',                   # test for shadow
        n.user_id, 'Receive 1 damage',                   # test for neutral
        s.user_id, 'Give an equipment card', 'Holy Robe' # test for giving equipment
    ])
    
    # Check that hunters do nothing
    init_hp = h.hp
    c.use({ 'self': s })
    assert h.hp == init_hp

    # Check that shadows take 1 damage
    init_hp = s.hp
    c.use({ 'self': h })
    assert s.hp == init_hp + 1

    # Check that neutrals take 1 damage
    init_hp = n.hp
    c.use({ 'self': h })
    assert n.hp == init_hp + 1

    # Check that giving equipment works
    eq = helpers.get_card_by_title(ef, 'Holy Robe')
    s.equipment.append(eq)
    init_hp = s.hp
    c.use({ 'self': h })
    assert s.hp == init_hp
    assert not s.equipment
    assert h.equipment == [eq]

def test_hermit_anger():
    
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Anger")
    gc.ask_h = helpers.answer_sequence([
        h.user_id, 'Receive 1 damage',                   # test for hunter
        s.user_id, 'Receive 1 damage',                   # test for shadow
        n.user_id, 'Do nothing',                         # test for neutral
        s.user_id, 'Give an equipment card', 'Holy Robe' # test for giving equipment
    ])
    
    # Check that hunters take 1 damage
    init_hp = h.hp
    c.use({ 'self': s })
    assert h.hp == init_hp + 1

    # Check that shadows take 1 damage
    init_hp = s.hp
    c.use({ 'self': h })
    assert s.hp == init_hp + 1

    # Check that neutrals do nothing
    init_hp = n.hp
    c.use({ 'self': h })
    assert n.hp == init_hp

    # Check that giving equipment works
    eq = helpers.get_card_by_title(ef, 'Holy Robe')
    s.equipment.append(eq)
    init_hp = s.hp
    c.use({ 'self': h })
    assert s.hp == init_hp
    assert not s.equipment
    assert h.equipment == [eq]

def test_hermit_slap():
        
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Slap")
    gc.ask_h = helpers.answer_sequence([
        h.user_id, 'Receive 1 damage', # test for hunter
        s.user_id, 'Do nothing',       # test for shadow
        n.user_id, 'Do nothing'        # test for neutral
    ])
    
    # Check that hunters take 1 damage
    init_hp = h.hp
    c.use({ 'self': s })
    assert h.hp == init_hp + 1

    # Check that shadows do nothing
    init_hp = s.hp
    c.use({ 'self': h })
    assert s.hp == init_hp

    # Check that neutrals do nothing
    init_hp = n.hp
    c.use({ 'self': h })
    assert n.hp == init_hp

def test_hermit_spell():
    
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Spell")
    gc.ask_h = helpers.answer_sequence([
        h.user_id, 'Do nothing',       # test for hunter
        s.user_id, 'Receive 1 damage', # test for shadow
        n.user_id, 'Do nothing'        # test for neutral
    ])
    
    # Check that hunters do nothing
    init_hp = h.hp
    c.use({ 'self': s })
    assert h.hp == init_hp

    # Check that shadows take 1 damage
    init_hp = s.hp
    c.use({ 'self': h })
    assert s.hp == init_hp + 1

    # Check that neutrals do nothing
    init_hp = n.hp
    c.use({ 'self': h })
    assert n.hp == init_hp

def test_hermit_exorcism():
    
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Exorcism")
    gc.ask_h = helpers.answer_sequence([
        h.user_id, 'Do nothing',       # test for hunter
        s.user_id, 'Receive 2 damage', # test for shadow
        n.user_id, 'Do nothing'        # test for neutral
    ])

    # Check that hunters do nothing
    init_hp = h.hp
    c.use({ 'self': s })
    assert h.hp == init_hp

    # Check that shadows take 2 damage
    init_hp = s.hp
    c.use({ 'self': h })
    assert s.hp == init_hp + 2

    # Check that neutrals do nothing
    init_hp = n.hp
    c.use({ 'self': h })
    assert n.hp == init_hp

def test_hermit_nurturance():
    
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Nurturance")
    gc.ask_h = helpers.answer_sequence([
        h.user_id, 'Do nothing',       # test for hunter
        s.user_id, 'Do nothing',       # test for shadow
        n.user_id, 'Heal 1 damage',    # test for neutral
        n.user_id, 'Receive 1 damage'  # test for neutral (damage)
    ])
    
    # Check that hunters do nothing
    h.hp = 1
    c.use({ 'self': s })
    assert h.hp == 1

    # Check that shadows do nothing
    s.hp = 1
    c.use({ 'self': h })
    assert s.hp == 1

    # Check that neutrals heal 1 damage
    n.hp = 1
    c.use({ 'self': h })
    assert n.hp == 0

    # Check that neutrals take 1 damage when at 0
    c.use({ 'self': h })
    assert n.hp == 1

def test_hermit_aid():
    
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Aid")
    gc.ask_h = helpers.answer_sequence([
        h.user_id, 'Heal 1 damage',    # test for hunter
        s.user_id, 'Do nothing',       # test for shadow
        n.user_id, 'Do nothing',       # test for neutral
        h.user_id, 'Receive 1 damage'  # test for hunter (damage)
    ])

    # Check that hunters heal 1 damage
    h.hp = 1
    c.use({ 'self': s })
    assert h.hp == 0

    # Check that shadows do nothing
    s.hp = 1
    c.use({ 'self': h })
    assert s.hp == 1

    # Check that neutrals do nothing
    n.hp = 1
    c.use({ 'self': h })
    assert n.hp == 1

    # Check that hunters take 1 damage when at 0
    c.use({ 'self': s })
    assert h.hp == 1

def test_hermit_fiddle():
    
    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Fiddle")
    gc.ask_h = helpers.answer_sequence([
        h.user_id, 'Do nothing',       # test for hunter
        s.user_id, 'Heal 1 damage',    # test for shadow
        n.user_id, 'Do nothing',       # test for neutral
        s.user_id, 'Receive 1 damage'  # test for shadow (damage)
    ])

    # Check that hunters do nothing
    h.hp = 1
    c.use({ 'self': s })
    assert h.hp == 1

    # Check that shadows heal 1 damage
    s.hp = 1
    c.use({ 'self': h })
    assert s.hp == 0

    # Check that neutrals do nothing
    n.hp = 1
    c.use({ 'self': h })
    assert n.hp == 1

    # Check that shadows take 1 damage when at 0
    c.use({ 'self': h })
    assert s.hp == 1 
