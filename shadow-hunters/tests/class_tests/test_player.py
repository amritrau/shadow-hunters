from tests import helpers
import pytest

import player
import area
import character
import game_context
import elements

# test_player.py
# Tests for the player object

def test_fields():

    # test initialization
    p = player.Player('Max', 'socket_id', lambda x, y, z: 5, False)

    # test fields
    assert p.user_id == 'Max'
    assert p.socket_id == 'socket_id'
    assert not p.gc
    assert p.state == 2
    assert not p.character
    assert not p.location
    assert not p.equipment
    assert not p.modifiers
    assert p.damage == 0
    assert p.ai == False
    assert p.ask_h(0, 0, 0) == 5

    # test dump
    dump = p.dump()
    assert (dump == {
        'user_id': 'Max',
        'socket_id': 'socket_id',
        'state': 2,
        'equipment': [],
        'damage': 0,
        'location': {},
        'character': {},
        'modifiers': {},
        'ai': False
    })

def test_setCharacter():
    p = player.Player('Max', 'socket_id', lambda x, y, z: 5, False)

    # dummy character
    c = character.Character(
        name = "char_name",
        alleg = 1,
        max_damage = 10,
        win_cond = lambda: 5,
        win_cond_desc = "win_desc",
        special = lambda: 5,
        resource_id = "r_id"
    )

    # Check that setting a character updates player character
    p.setCharacter(c)
    assert p.character == c

def test_reveal():
    p = helpers.fresh_gc_ef()[0].players[0]

    # Check that reveal sets state to 1
    p.reveal()
    assert p.state == 1

def test_takeTurn():
    # TODO: Unclear how to meaningfully test this function
    assert 1

def test_drawCard():
    # TODO: Unclear how to meaningfully test this function
    assert 1

def test_attack():
    # TODO: Test unwritten because implementation is subject to change
    assert 1

def test_defend():
    # TODO: Test unwritten because implementation is subject to change
    assert 1

def test_moveDamage():
    p = helpers.fresh_gc_ef()[0].players[0]

    # Check in-bounds movement
    p.moveDamage(-5)
    assert p.damage == 5

    # Check ceiling of max_damage
    p.moveDamage(-50)
    assert p.damage == p.character.max_damage

    # Check floor of 0
    p.moveDamage(100)
    assert p.damage == 0

def test_setDamage():
    p = helpers.fresh_gc_ef()[0].players[0]

    # Check setting damage changes player damage
    p.setDamage(5)
    assert p.damage == 5

def test_checkDeath():
    p = helpers.fresh_gc_ef()[0].players[0]

    # Check that player is initially not dead
    p.checkDeath()
    assert p.state == 2

    # Check that player dies when damage > max_damage
    p.damage = 20
    p.checkDeath()
    assert p.state == 0

def test_move():
    p = helpers.fresh_gc_ef()[0].players[0]

    # dummy area
    a = area.Area(
        name = "area_name",
        desc = "area_desc",
        domain = [9],
        action = lambda: 5,
        resource_id = "r_id"
    )

    # Check that moving to a location updates player location
    p.move(a)
    assert p.location == a
