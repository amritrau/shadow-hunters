import pytest
import random

import game_context
import player
import helpers

# test_white_cards.py
# Tests the usage of each white single-use card

def test_flare_judgement():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    c = helpers.get_card_by_title(ef, "Flare of Judgement")

    # Check that flare hits everyone for 2 except you
    c.use({ 'self': p1, 'card': c })
    for p in gc.players:
        if p != p1:
            assert p.damage == 2
        else:
            assert p.damage == 0

def test_first_aid():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    c = helpers.get_card_by_title(ef, "First Aid")

    # Check that someone gets set to 7 by first aid and everyone else is unaffected
    c.use({ 'self': p1, 'card': c })
    damages = [p.damage for p in gc.players]
    assert len([d for d in damages if d == 7]) == 1
    assert len([d for d in damages if d == 0]) == len(gc.players) - 1

def test_holy_water():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    c = helpers.get_card_by_title(ef, "Holy Water of Healing")

    # Check that holy water heals you by 2
    p1.damage = 4
    c.use({ 'self': p1, 'card': c })
    assert p1.damage == 2

def test_advent():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef(random.randint(5,8))
    h = helpers.get_a_hunter(gc)
    s = helpers.get_a_shadow(gc)
    n = helpers.get_a_neutral(gc)
    c = helpers.get_card_by_title(ef, "Advent")

    # Check that shadows do nothing
    s.damage = 3
    c.use({ 'self': s, 'card': c })
    assert s.state == 2 and s.damage == 3

    # Check that neutrals do nothing
    n.damage = 3
    c.use({ 'self': n, 'card': c })
    assert n.state == 2 and n.damage == 3

    # Hunter do nothing
    gc.ask_h = helpers.answer_sequence(['Do nothing', 'Reveal and heal fully', 'Heal fully'])
    h.damage = 3
    c.use({ 'self': h, 'card': c })
    assert h.state == 2 and h.damage == 3

    # Hunter reveal and full heal
    c.use({ 'self': h, 'card': c })
    assert h.state == 1 and h.damage == 0

    # Hunter full heal
    h.damage = 3
    c.use({ 'self': h, 'card': c })
    assert h.state == 1 and h.damage == 0

def test_blessing():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    c = helpers.get_card_by_title(ef, "Blessing")

    # Check that user is not healed, but someone is and everyone else is unaffected
    for p in gc.players:
        p.damage = 6
    c.use({ 'self': p1, 'card': c })
    damages = [p.damage for p in gc.players]
    assert p1.damage == 6
    assert len([d for d in damages if d < 6]) == 1
    assert len([d for d in damages if d == 6]) == len(gc.players) - 1


def test_disenchant_mirror():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef(random.randint(5,8))
    h = helpers.get_a_hunter(gc)
    s = helpers.get_a_shadow(gc)
    n = helpers.get_a_neutral(gc)
    c = helpers.get_card_by_title(ef, "Disenchant Mirror")

    # Check that shadows reveal
    c.use({ 'self': s, 'card': c })
    assert s.state == 1

    # Check that hunters do nothing
    c.use({ 'self': h, 'card': c })
    assert h.state == 2

    # Check that neutrals do nothing
    c.use({ 'self': n, 'card': c })
    assert n.state == 2

def test_chocolate():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef(7)
    weak = [p for p in gc.players if p.character.name in ["Allie", "Ellen", "Ultra Soul"]][0]
    strong = [p for p in gc.players if p.character.name not in ["Allie", "Ellen", "Ultra Soul"]][0]
    c = helpers.get_card_by_title(ef, "Chocolate")

    # Strong player do nothing
    strong.damage = 3
    c.use({ 'self': strong, 'card': c })
    assert strong.state == 2 and strong.damage == 3

    # Weak player do nothing
    gc.ask_h = helpers.answer_sequence(['Do nothing', 'Reveal and heal fully', 'Heal fully'])
    weak.damage = 3
    c.use({ 'self': weak, 'card': c })
    assert weak.state == 2 and weak.damage == 3

    # Weak player reveal and full heal
    c.use({ 'self': weak, 'card': c })
    assert weak.state == 1 and weak.damage == 0

    # Weak player full heal
    weak.damage = 3
    c.use({ 'self': weak, 'card': c })
    assert weak.state == 1 and weak.damage == 0

def test_concealed_knowledge():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef(8)
    position = random.randint(0,7)
    p1 = gc.players[position]
    c = helpers.get_card_by_title(ef, "Concealed Knowledge")

    # Check that card inserts player in proper place
    c.use({ 'self': p1, 'card': c })
    assert gc.turn_order[position] == p1 and gc.turn_order[position+1] == p1

def test_guardian_angel():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    p2 = gc.players[1]
    c = helpers.get_card_by_title(ef, "Guardian Angel")

    # Check that p1 is immune to direct attacks
    c.use({ 'self': p1, 'card': c })
    assert p1.modifiers['guardian_angel']
    p2.attack(p1, 5)
    assert p1.damage == 0
