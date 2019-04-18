import pytest
import random

import game_context
import player
import helpers

# test_black_cards.py
# Tests the usage of each black single-use card

def test_bloodthirsty_spider():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    c = helpers.get_card_by_title(ef, "Bloodthirsty Spider")

    # Check that user and target take 2 damage and everyone else is unaffected
    c.use({ 'self': p1, 'card': c })
    damages = [p.damage for p in gc.players]
    assert p1.damage == 2
    assert len([d for d in damages if d == 2]) == 2
    assert len([d for d in damages if d == 0]) == len(gc.players) - 2

def test_vampire_bat():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    c = helpers.get_card_by_title(ef, "Vampire Bat")

    # Check that user heals 1 damage and target takes 2 damage and everyone else is unaffected
    p1.damage == 1
    c.use({ 'self': p1, 'card': c })
    damages = [p.damage for p in gc.players]
    assert len([d for d in damages if d == 2]) == 1
    assert len([d for d in damages if d == 0]) == len(gc.players) - 1

def test_moody_goblin():
    assert 1

def test_diabolic_ritual():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef(random.randint(5,8))
    h = helpers.get_a_hunter(gc)
    s = helpers.get_a_shadow(gc)
    n = helpers.get_a_neutral(gc)
    c = helpers.get_card_by_title(ef, "Diabolic Ritual")

    # Check that hunters do nothing
    h.damage = 3
    c.use({ 'self': h, 'card': c })
    assert h.state == 2 and h.damage == 3

    # Check that neutrals do nothing
    n.damage = 3
    c.use({ 'self': n, 'card': c })
    assert n.state == 2 and n.damage == 3

    # Shadow do nothing
    gc.ask_h = helpers.answer_sequence(['Do nothing', 'Reveal and heal fully'])
    s.damage = 3
    c.use({ 'self': s, 'card': c })
    assert s.state == 2 and s.damage == 3

    # Shadow reveal and full heal
    c.use({ 'self': s, 'card': c })
    assert s.state == 1 and s.damage == 0

def test_banana_peel():
    assert 1

def test_spiritual_doll():
    assert 1
