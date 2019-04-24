import helpers
import pytest
import copy

import player
import area
import character
import game_context
import elements

# test_player.py
# Tests for the player object


def test_fields():

    # test initialization
    p = player.Player('Max', 'socket_id', 'c', False)

    # test fields
    assert p.user_id == 'Max'
    assert p.socket_id == 'socket_id'
    assert p.color == 'c'
    assert not p.gc
    assert p.state == 2
    assert not p.character
    assert not p.location
    assert not p.equipment
    assert p.modifiers['attack_dice_type'] == 'attack'
    assert p.damage == 0
    assert not p.ai

    # test dump
    dump = p.dump()
    assert dump['user_id'] == 'Max'
    assert dump['socket_id'] == 'socket_id'
    assert dump['state'] == 2
    assert dump['equipment'] == []
    assert dump['damage'] == 0
    assert dump['location'] == {}
    assert dump['character'] == {}
    assert not dump['ai']


def test_setCharacter():
    p = player.Player('Max', 'socket_id', lambda x, y, z: 5, False)

    # dummy character
    c = character.Character(
        name="char_name",
        alleg=1,
        max_damage=10,
        win_cond=lambda: 5,
        win_cond_desc="win_desc",
        special_desc="special_desc",
        special=lambda: 5,
        resource_id="r_id"
    )

    # Check that setting a character updates player character
    p.setCharacter(c)
    assert p.character == c


def test_reveal():
    p = helpers.fresh_gc_ef()[0].players[0]

    # Check that reveal sets state to 1
    p.reveal()
    assert p.state == 1


def test_drawCard():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]

    # Draw white card
    original_deck = copy.copy(gc.white_cards.cards)
    assert gc.white_cards.cards == original_deck
    p1.drawCard(gc.white_cards)
    assert gc.white_cards.cards != original_deck

    # Draw black card
    original_deck = copy.copy(gc.black_cards.cards)
    assert gc.black_cards.cards == original_deck
    p1.drawCard(gc.black_cards)
    assert gc.black_cards.cards != original_deck

    # Draw hermit card
    original_deck = copy.copy(gc.green_cards.cards)
    assert gc.green_cards.cards == original_deck
    p1.drawCard(gc.green_cards)
    assert gc.green_cards.cards != original_deck


def test_rollDice():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]

    # Check 4-sided rolls
    for _ in range(100):
        assert 1 <= p1.rollDice('4') <= 4

    # Check 6-sided rolls
    for _ in range(100):
        assert 1 <= p1.rollDice('6') <= 6

    # Check movement rolls
    for _ in range(100):
        assert 2 <= p1.rollDice('area') <= 10

    # Check attack rolls
    for _ in range(100):
        assert 0 <= p1.rollDice('attack') <= 5


def test_choosePlayer():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]

    # Check that chosen player is in gc and not self
    for _ in range(100):
        p2 = p1.choosePlayer()
        assert p2 in gc.players and p2 != p1


def test_chooseEquipment():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    p2 = gc.players[1]
    roly_hobe = helpers.get_card_by_title(ef, "Holy Robe")
    talisman = helpers.get_card_by_title(ef, "Talisman")
    p1.equipment = [roly_hobe, talisman]

    # Check that p2 always chooses an equipment from the options
    for _ in range(100):
        eq = p2.chooseEquipment(p1)
        assert eq == roly_hobe or eq == talisman


def test_giveEquipment():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    p2 = gc.players[1]
    roly_hobe = helpers.get_card_by_title(ef, "Holy Robe")
    p1.equipment.append(roly_hobe)

    # P1 gives holy robe to P2
    p1.giveEquipment(p2, roly_hobe)

    # Check that P1 lost holy robe, check that P2 got it
    assert roly_hobe.holder == p2
    assert not p1.equipment
    assert roly_hobe in p2.equipment


def test_attack():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    p2 = gc.players[1]

    # Check that damage is dealt properly
    p1.attack(p2, 5)
    assert p2.damage == 5

    # Check that equipment works
    p2.damage = 0
    p1.equipment = [
        helpers.get_card_by_title(ef, "Holy Robe"),
        helpers.get_card_by_title(ef, "Chainsaw"),
        helpers.get_card_by_title(ef, "Butcher Knife")
    ]
    p1.attack(p2, 5)
    assert p2.damage == 6

    # Check that equipment doesn't work if attack is unsuccessful
    p2.damage = 0
    p1.attack(p2, 0)
    assert p2.damage == 0


def test_defend():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    p2 = gc.players[1]

    # Check that damage is dealt properly
    p1.defend(p2, 5)
    assert p1.damage == 5


def test_moveDamage():
    p = helpers.fresh_gc_ef()[0].players[0]

    # Check in-bounds movement
    p.moveDamage(-5, p)
    assert p.damage == 5

    # Check ceiling of max_damage
    p.moveDamage(-50, p)
    assert p.damage == p.character.max_damage

    # Check floor of 0
    p.moveDamage(100, p)
    assert p.damage == 0


def test_setDamage():
    p = helpers.fresh_gc_ef()[0].players[0]

    # Check setting damage changes player damage
    p.setDamage(5, p)
    assert p.damage == 5


def test_checkDeath():
    p = helpers.fresh_gc_ef()[0].players[0]

    # Check that player is initially not dead
    p.checkDeath(p)
    assert p.state == 2

    # Check that player dies when damage > max_damage
    p.damage = 20
    p.checkDeath(p)
    assert p.state == 0


def test_die():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]
    p2 = gc.players[1]
    talisman = helpers.get_card_by_title(ef, "Talisman")
    roly_hobe = helpers.get_card_by_title(ef, "Holy Robe")
    p1.equipment = [roly_hobe, talisman]

    # Player 1 dies by player 2
    p1.die(p2)

    # Check that player 1 is dead, location is none, loses all equipment, and
    # gives one to player 2
    assert p1.state == 0
    assert not p1.equipment
    assert bool(roly_hobe in p2.equipment) != bool(talisman in p2.equipment)
    assert p1.location is None


def test_move():

    # Setup rigged game context
    gc, ef = helpers.fresh_gc_ef()
    p1 = gc.players[0]

    # Check that moving to a location updates player location
    a = helpers.get_area_by_name(gc, "Weird Woods")
    p1.move(a)
    assert p1.location == a
