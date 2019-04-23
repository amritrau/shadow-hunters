import pytest
import random
import copy

import game_context
import player
import helpers

# test_area_actions.py
# Tests the possible actions at each area

# Tests on hermit's cabin, church, and cemetery
# are subsumed by tests of player.drawCard()


def test_weird_woods():

    # Set up rigged game context
    gc, ef = helpers.fresh_gc_ef()
    area = helpers.get_area_by_name(gc, "Weird Woods")

    target = helpers.get_a_shadow(gc)
    actor = helpers.get_a_hunter(gc)

    gc.ask_h = helpers.answer_sequence([
        target.user_id, 'Give 2 damage',  # test damage
        target.user_id, 'Heal 1 damage',  # test heal
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
        target.user_id, 'Holy Robe'  # test pick an equipment to steal
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


def test_underworld_gate():

    # Set up rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    area = helpers.get_area_by_name(gc, "Underworld Gate")
    whites = copy.copy(gc.white_cards.cards)
    blacks = copy.copy(gc.black_cards.cards)
    greens = copy.copy(gc.green_cards.cards)

    # Make sure one of the card piles was taken from
    area.action(gc, p1)
    white_check = (gc.white_cards.cards != whites)
    black_check = (gc.black_cards.cards != blacks)
    green_check = (gc.green_cards.cards != greens)
    assert white_check or black_check or green_check
