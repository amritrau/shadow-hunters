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

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    p2 = gc.players[1]
    c = helpers.get_card_by_title(ef, "Moody Goblin")

    # Check that nothing happens if no one has equipment
    c.use({ 'self': p2, 'card': c })
    assert not p2.equipment

    # Give p1 holy robe
    roly_hobe = helpers.get_card_by_title(ef, "Holy Robe")
    p1.equipment.append(roly_hobe)

    # Check that robe is stolen
    c.use({ 'self': p2, 'card': c })
    assert p2.equipment == [roly_hobe]
    assert not p1.equipment

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

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    p2 = gc.players[1]
    gc.ask_h = helpers.answer_sequence([
        "Receive 1 damage",
        "Give an equipment card",
        "Holy Robe",
        p2.user_id
    ])
    c = helpers.get_card_by_title(ef, "Banana Peel")

    # Give p1 holy robe
    roly_hobe = helpers.get_card_by_title(ef, "Holy Robe")
    p1.equipment.append(roly_hobe)

    # Check take one damage
    assert p1.damage == 0
    c.use({ 'self': p1, 'card': c })
    assert p1.damage == 1

    # Check give away equipment
    c.use({ 'self': p1, 'card': c })
    assert p1.damage == 1
    assert not p1.equipment
    assert p2.equipment == [roly_hobe]

def test_dynamite():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef(6)
    p1 = gc.players[0]
    c = helpers.get_card_by_title(ef, "Dynamite")

    # Put one player in each area
    area_names = ["Church", "Cemetery", "Erstwhile Altar", "Weird Woods", "Hermit\'s Cabin", "Underworld Gate"]
    areas = [helpers.get_area_by_name(gc, a) for a in area_names]
    for p in gc.players:
        p.move(areas.pop(0))

    # Check that only one person took 3 damage
    c.use({ 'self': p1, 'card': c })
    damages = [p.damage for p in gc.players]
    assert len([d for d in damages if d == 3]) <= 1
    assert len([d for d in damages if d == 0]) == len(gc.players) - 1


def test_spiritual_doll():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    p2 = gc.players[1]
    c = helpers.get_card_by_title(ef, "Spiritual Doll")
    gc.ask_h = helpers.answer_sequence([
        "Use Spiritual Doll",
        p2.user_id,
        "Roll the 6-sided die!"
    ])

    # Check that someone gets hit
    c.use({ 'self': p1, 'card': c })
    assert bool(p1.damage == 3) != bool(p2.damage == 3)
