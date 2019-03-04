from tests import helpers
import pytest

import player
import area
import character
import game_context
import cli

# test_player.py
# Tests for the player object

def test_fields():
    
    # test initialization
    p = player.Player('Max', 'socket_id')

    # test fields
    assert p.user_id == 'Max'
    assert p.socket_id == 'socket_id'
    assert not p.gc
    assert p.state == 2
    assert not p.character
    assert not p.location
    assert not p.equipment
    assert not p.modifiers
    assert p.hp == 0

    # test dump
    dump = p.dump()
    assert (dump == {
        'user_id': 'Max',
        'socket_id': 'socket_id',
        'state': 2,
        'equipment': [],
        'hp': 0,
        'location': {},
        'character': {},
        'modifiers': {}
    })

def test_setCharacter():
    p = player.Player('Max', 'socket_id')
    
    # dummy character
    c = character.Character(
        name = "char_name",
        alleg = 1,
        max_hp = 10,
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
    assert 1

def test_drawCard():
    assert 1

def test_attack():
    assert 1

def test_defend():
    assert 1

def test_moveHP():
    p = helpers.fresh_gc_ef()[0].players[0]

    # Check in-bounds movement
    p.moveHP(-5)
    assert p.hp == 5

    # Check ceiling of max_hp
    p.moveHP(-50)
    assert p.hp == p.character.max_hp

    # Check floor of 0
    p.moveHP(100)
    assert p.hp == 0

def test_setHP():
    p = helpers.fresh_gc_ef()[0].players[0]
    
    # Check setting hp changes player hp
    p.setHP(5)
    assert p.hp == 5

def test_checkDeath():
    p = helpers.fresh_gc_ef()[0].players[0]
    
    # Check that player is initially not dead
    p.checkDeath()
    assert p.state == 2

    # Check that player dies when hp > max_hp
    p.hp = 20
    p.checkDeath()
    assert p.state == 0

def test_move():
    p = player.Player('Max', 'socket_id')
    
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
