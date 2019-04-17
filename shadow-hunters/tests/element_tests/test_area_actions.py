import pytest
import random

import game_context
import player
import helpers

# test_area_actions.py
# Tests the possible actions at each area

# Tests on hermit's cabin, church, and cemetery
# are subsumed by tests of player.drawCard()

def test_underworld_gate():
    assert 1

def test_weird_woods():

    # Set up rigged game context
    gc, ef = helpers.fresh_gc_ef()
    area = helpers.get_area_by_name(gc, "Weird Woods")

    target = helpers.get_a_shadow(gc)
    actor = helpers.get_a_hunter(gc)

    gc.ask_h = helpers.answer_sequence([
        target.user_id, 'Give 2 damage', # test damage
        target.user_id, 'Heal 1 damage', # test heal
    ])

    # Check give 2 damage
    area.action(gc, actor)
    assert target.damage == 2

    # Check heal 1 damage
    area.action(gc, actor)
    assert target.damage == 1

def test_erstwhile_altar():

    # Set up rigged game context
    gc, ef = helpers.fresh_gc_ef()
    area = helpers.get_area_by_name(gc, "Erstwhile Altar")

    target = helpers.get_a_shadow(gc)
    actor = helpers.get_a_hunter(gc)

    gc.ask_h = helpers.answer_sequence([
        target.user_id, 'Holy Robe' # test pick an equipment to steal
    ])

    # Check that nothing happens if no one has equipment
    area.action(gc, actor)
    assert all([len(p.equipment) == 0 for p in gc.players])

    # Check that nothing happens if only current player has equipment
    chainsaw = helpers.get_card_by_title(ef, "Chainsaw")
    actor.equipment.append(chainsaw)
    area.action(gc, actor)
    assert all([len(p.equipment) == 0 for p in gc.players if p != actor])
    assert actor.equipment == [chainsaw]

    # Check that selected equipment is stolen from selected player
    axe = helpers.get_card_by_title(ef, "Rusted Broad Axe")
    roly_hobe = helpers.get_card_by_title(ef, "Holy Robe")
    target.equipment.append(axe)
    target.equipment.append(roly_hobe)
    area.action(gc, actor)
    assert actor.equipment == [chainsaw, roly_hobe]
    assert target.equipment == [axe]
