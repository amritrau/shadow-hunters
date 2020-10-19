import pytest

import helpers as H
import copy

# test_area_actions.py
# Tests the possible actions at each area

# Tests on hermit's cabin, church, and cemetery
# are subsumed by tests of player.drawCard()


def test_weird_woods():

    # Set up rigged game context
    gc, ef = H.fresh_gc_ef()
    area = H.get_area_by_name(gc, "Weird Woods")

    target = H.get_a_shadow(gc)
    actor = H.get_a_hunter(gc)

    gc.ask_h = H.answer_sequence([
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
    gc, ef = H.fresh_gc_ef()
    area = H.get_area_by_name(gc, "Erstwhile Altar")

    target = H.get_a_shadow(gc)
    actor = H.get_a_hunter(gc)

    gc.ask_h = H.answer_sequence([
        target.user_id, 'Holy Robe'  # test pick an equipment to steal
    ])

    # Check that nothing happens if no one has equipment
    area.action(gc, actor)
    assert all([len(p.equipment) == 0 for p in gc.players])

    # Check that nothing happens if only current player has equipment
    chainsaw = H.get_card_by_title(ef, "Chainsaw")
    actor.equipment.append(chainsaw)
    area.action(gc, actor)
    assert all([len(p.equipment) == 0 for p in gc.players if p != actor])
    assert actor.equipment == [chainsaw]

    # Check that selected equipment is stolen from selected player
    axe = H.get_card_by_title(ef, "Rusted Broad Axe")
    roly_hobe = H.get_card_by_title(ef, "Holy Robe")
    target.equipment.append(axe)
    target.equipment.append(roly_hobe)
    area.action(gc, actor)
    assert actor.equipment == [chainsaw, roly_hobe]
    assert target.equipment == [axe]


def test_underworld_gate():

    # Set up rigged game context
    gc, ef = H.fresh_gc_ef()
    p1 = gc.players[0]
    area = H.get_area_by_name(gc, "Underworld Gate")
    whites = copy.copy(gc.white_cards.cards)
    blacks = copy.copy(gc.black_cards.cards)
    greens = copy.copy(gc.green_cards.cards)

    # Make sure one of the card piles was taken from
    area.action(gc, p1)
    neq_whites = gc.white_cards.cards != whites
    neq_blacks = gc.black_cards.cards != blacks
    neq_greens = gc.green_cards.cards != greens
    assert neq_whites or neq_blacks or neq_greens
