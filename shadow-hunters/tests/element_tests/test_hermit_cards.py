import pytest
import random

import game_context
import player
import helpers

# test_hermit_cards.py
# Tests the usage of each hermit card

def setup_hermit(title, n_players = random.randint(5,8)):
    """
    Return a game context, element factory, a hunter, shadow
    and neutral from that game, and a card of a given title
    """
    gc, ef = helpers.fresh_gc_ef(n_players)
    h = helpers.get_a_hunter(gc)
    s = helpers.get_a_shadow(gc)
    n = helpers.get_a_neutral(gc)
    c = helpers.get_card_by_title(ef, title)
    return (gc, ef, h, s, n, c)

def test_hermit_blackmail():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Blackmail")
    gc.ask_h = helpers.answer_sequence([
        "Use Hermit\'s Blackmail",
        h.user_id, 'Receive 1 damage',                   # test for hunter
        "Use Hermit\'s Blackmail",
        s.user_id, 'Do nothing',                         # test for shadow
        "Use Hermit\'s Blackmail",
        n.user_id, 'Receive 1 damage',                   # test for neutral
        "Use Hermit\'s Blackmail",
        h.user_id, 'Give an equipment card', 'Holy Robe' # test for giving equipment
    ])

    # Check that hunters take 1 damage
    init_damage = h.damage
    c.use({ 'self': s, 'card': c })
    assert h.damage == init_damage + 1

    # Check that shadows do nothing
    init_damage = s.damage
    c.use({ 'self': h, 'card': c })
    assert s.damage == init_damage

    # Check that neutrals take 1 damage
    init_damage = n.damage
    c.use({ 'self': h, 'card': c })
    assert n.damage == init_damage + 1

    # Check that giving equipment works
    eq = helpers.get_card_by_title(ef, 'Holy Robe')
    h.equipment.append(eq)
    init_damage = h.damage
    c.use({ 'self': s, 'card': c })
    assert h.damage == init_damage
    assert not h.equipment
    assert s.equipment == [eq]

def test_hermit_greed():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Greed")
    gc.ask_h = helpers.answer_sequence([
        "Use Hermit\'s Greed",
        h.user_id, 'Do nothing',                         # test for hunter
        "Use Hermit\'s Greed",
        s.user_id, 'Receive 1 damage',                   # test for shadow
        "Use Hermit\'s Greed",
        n.user_id, 'Receive 1 damage',                   # test for neutral
        "Use Hermit\'s Greed",
        s.user_id, 'Give an equipment card', 'Holy Robe' # test for giving equipment
    ])

    # Check that hunters do nothing
    init_damage = h.damage
    c.use({ 'self': s, 'card': c })
    assert h.damage == init_damage

    # Check that shadows take 1 damage
    init_damage = s.damage
    c.use({ 'self': h, 'card': c })
    assert s.damage == init_damage + 1

    # Check that neutrals take 1 damage
    init_damage = n.damage
    c.use({ 'self': h, 'card': c })
    assert n.damage == init_damage + 1

    # Check that giving equipment works
    eq = helpers.get_card_by_title(ef, 'Holy Robe')
    s.equipment.append(eq)
    init_damage = s.damage
    c.use({ 'self': h, 'card': c })
    assert s.damage == init_damage
    assert not s.equipment
    assert h.equipment == [eq]

def test_hermit_anger():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Anger")
    gc.ask_h = helpers.answer_sequence([
        "Use Hermit\'s Anger",
        h.user_id, 'Receive 1 damage',                   # test for hunter
        "Use Hermit\'s Anger",
        s.user_id, 'Receive 1 damage',                   # test for shadow
        "Use Hermit\'s Anger",
        n.user_id, 'Do nothing',                         # test for neutral
        "Use Hermit\'s Anger",
        s.user_id, 'Give an equipment card', 'Holy Robe' # test for giving equipment
    ])

    # Check that hunters take 1 damage
    init_damage = h.damage
    c.use({ 'self': s, 'card': c })
    assert h.damage == init_damage + 1

    # Check that shadows take 1 damage
    init_damage = s.damage
    c.use({ 'self': h, 'card': c })
    assert s.damage == init_damage + 1

    # Check that neutrals do nothing
    init_damage = n.damage
    c.use({ 'self': h, 'card': c })
    assert n.damage == init_damage

    # Check that giving equipment works
    eq = helpers.get_card_by_title(ef, 'Holy Robe')
    s.equipment.append(eq)
    init_damage = s.damage
    c.use({ 'self': h, 'card': c })
    assert s.damage == init_damage
    assert not s.equipment
    assert h.equipment == [eq]

def test_hermit_slap():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Slap")
    gc.ask_h = helpers.answer_sequence([
        "Use Hermit\'s Slap",
        h.user_id, 'Receive 1 damage', # test for hunter
        "Use Hermit\'s Slap",
        s.user_id, 'Do nothing',       # test for shadow
        "Use Hermit\'s Slap",
        n.user_id, 'Do nothing'        # test for neutral
    ])

    # Check that hunters take 1 damage
    init_damage = h.damage
    c.use({ 'self': s, 'card': c })
    assert h.damage == init_damage + 1

    # Check that shadows do nothing
    init_damage = s.damage
    c.use({ 'self': h, 'card': c })
    assert s.damage == init_damage

    # Check that neutrals do nothing
    init_damage = n.damage
    c.use({ 'self': h, 'card': c })
    assert n.damage == init_damage

def test_hermit_spell():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Spell")
    gc.ask_h = helpers.answer_sequence([
        "Use Hermit\'s Spell",
        h.user_id, 'Do nothing',       # test for hunter
        "Use Hermit\'s Spell",
        s.user_id, 'Receive 1 damage', # test for shadow
        "Use Hermit\'s Spell",
        n.user_id, 'Do nothing'        # test for neutral
    ])

    # Check that hunters do nothing
    init_damage = h.damage
    c.use({ 'self': s, 'card': c })
    assert h.damage == init_damage

    # Check that shadows take 1 damage
    init_damage = s.damage
    c.use({ 'self': h, 'card': c })
    assert s.damage == init_damage + 1

    # Check that neutrals do nothing
    init_damage = n.damage
    c.use({ 'self': h, 'card': c })
    assert n.damage == init_damage

def test_hermit_exorcism():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Exorcism")
    gc.ask_h = helpers.answer_sequence([
        "Use Hermit\'s Exorcism",
        h.user_id, 'Do nothing',       # test for hunter
        "Use Hermit\'s Exorcism",
        s.user_id, 'Receive 2 damage', # test for shadow
        "Use Hermit\'s Exorcism",
        n.user_id, 'Do nothing'        # test for neutral
    ])

    # Check that hunters do nothing
    init_damage = h.damage
    c.use({ 'self': s, 'card': c })
    assert h.damage == init_damage

    # Check that shadows take 2 damage
    init_damage = s.damage
    c.use({ 'self': h, 'card': c })
    assert s.damage == init_damage + 2

    # Check that neutrals do nothing
    init_damage = n.damage
    c.use({ 'self': h, 'card': c })
    assert n.damage == init_damage

def test_hermit_nurturance():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Nurturance")
    gc.ask_h = helpers.answer_sequence([
        "Use Hermit\'s Nurturance",
        h.user_id, 'Do nothing',       # test for hunter
        "Use Hermit\'s Nurturance",
        s.user_id, 'Do nothing',       # test for shadow
        "Use Hermit\'s Nurturance",
        n.user_id, 'Heal 1 damage',    # test for neutral
        "Use Hermit\'s Nurturance",
        n.user_id, 'Receive 1 damage'  # test for neutral (damage)
    ])

    # Check that hunters do nothing
    h.damage = 1
    c.use({ 'self': s, 'card': c })
    assert h.damage == 1

    # Check that shadows do nothing
    s.damage = 1
    c.use({ 'self': h, 'card': c })
    assert s.damage == 1

    # Check that neutrals heal 1 damage
    n.damage = 1
    c.use({ 'self': h, 'card': c })
    assert n.damage == 0

    # Check that neutrals take 1 damage when at 0
    c.use({ 'self': h, 'card': c })
    assert n.damage == 1

def test_hermit_aid():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Aid")
    gc.ask_h = helpers.answer_sequence([
        "Use Hermit\'s Aid",
        h.user_id, 'Heal 1 damage',    # test for hunter
        "Use Hermit\'s Aid",
        s.user_id, 'Do nothing',       # test for shadow
        "Use Hermit\'s Aid",
        n.user_id, 'Do nothing',       # test for neutral
        "Use Hermit\'s Aid",
        h.user_id, 'Receive 1 damage'  # test for hunter (damage)
    ])

    # Check that hunters heal 1 damage
    h.damage = 1
    c.use({ 'self': s, 'card': c })
    assert h.damage == 0

    # Check that shadows do nothing
    s.damage = 1
    c.use({ 'self': h, 'card': c })
    assert s.damage == 1

    # Check that neutrals do nothing
    n.damage = 1
    c.use({ 'self': h, 'card': c })
    assert n.damage == 1

    # Check that hunters take 1 damage when at 0
    c.use({ 'self': s, 'card': c })
    assert h.damage == 1

def test_hermit_huddle():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Huddle")
    gc.ask_h = helpers.answer_sequence([
        "Use Hermit\'s Huddle",
        h.user_id, 'Do nothing',       # test for hunter
        "Use Hermit\'s Huddle",
        s.user_id, 'Heal 1 damage',    # test for shadow
        "Use Hermit\'s Huddle",
        n.user_id, 'Do nothing',       # test for neutral
        "Use Hermit\'s Huddle",
        s.user_id, 'Receive 1 damage'  # test for shadow (damage)
    ])

    # Check that hunters do nothing
    h.damage = 1
    c.use({ 'self': s, 'card': c })
    assert h.damage == 1

    # Check that shadows heal 1 damage
    s.damage = 1
    c.use({ 'self': h, 'card': c })
    assert s.damage == 0

    # Check that neutrals do nothing
    n.damage = 1
    c.use({ 'self': h, 'card': c })
    assert n.damage == 1

    # Check that shadows take 1 damage when at 0
    c.use({ 'self': h, 'card': c })
    assert s.damage == 1

def test_hermit_lesson():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Lesson", n_players=8)
    high_p = [p for p in gc.players if p.character.max_damage >= 12][0]
    low_p = [p for p in gc.players if p.character.max_damage <= 11][0]
    gc.ask_h = helpers.answer_sequence([
        "Use Hermit\'s Lesson",
        low_p.user_id, 'Do nothing',        # test for low hp
        "Use Hermit\'s Lesson",
        high_p.user_id, 'Receive 2 damage', # test for high hp
    ])

    # Check that characters with hp <= 11 do nothing
    init_damage = low_p.damage
    c.use({ 'self': high_p, 'card': c })
    assert low_p.damage == init_damage

    # Check that characters with hp >= 12 take 2 damage
    init_damage = high_p.damage
    c.use({ 'self': low_p, 'card': c })
    assert high_p.damage == init_damage + 2

def test_hermit_bully():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Bully", n_players=8)
    high_p = [p for p in gc.players if p.character.max_damage >= 12][0]
    low_p = [p for p in gc.players if p.character.max_damage <= 11][0]
    gc.ask_h = helpers.answer_sequence([
        "Use Hermit\'s Bully",
        high_p.user_id, 'Do nothing',      # test for high hp
        "Use Hermit\'s Bully",
        low_p.user_id, 'Receive 1 damage', # test for low hp
    ])

    # Check that characters with hp >= 12 do nothing
    init_damage = high_p.damage
    c.use({ 'self': low_p, 'card': c })
    assert high_p.damage == init_damage

    # Check that characters with hp <= 11 take 1 damage
    init_damage = low_p.damage
    c.use({ 'self': high_p, 'card': c })
    assert low_p.damage == init_damage + 1

def test_hermit_prediction():

    # setup rigged gc
    gc, ef, h, s, n, c = setup_hermit("Hermit\'s Prediction")
    gc.ask_h = helpers.answer_sequence([
        "Use Hermit\'s Prediction",
        h.user_id, 'Reveal',
    ])

    # Check that using the card works
    c.use({ 'self': s, 'card': c })

    # Effects no change on the game state
    assert 1
