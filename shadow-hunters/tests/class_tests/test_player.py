import pytest

import player
import area
import character
import game_context
import cli

# test_player.py
# Tests for the player object

# Helper function to give a player a character and game context
def init_player():
    p = player.Player('Max', 'socket_id')
    c = character.Character(
        name = "char_name",
        alleg = 1,
        max_hp = 10,
        win_cond = lambda: 5,
        win_cond_desc = "win_desc",
        special = lambda: 5,
        resource_id = "r_id"
    )
    p.setCharacter(c)
    player_names = ['Amrit', 'Max', 'Gia', 'Joanna', 'Vishal']
    players = [player.Player(user_id, socket_id='unused') for user_id in player_names]
    ef = cli.ElementFactory()
    gc = game_context.GameContext(
        players = players,
        characters = ef.CHARACTERS,
        black_cards = ef.BLACK_DECK,
        white_cards = ef.WHITE_DECK,
        green_cards = ef.GREEN_DECK,
        areas = ef.AREAS,
        tell_h = lambda x: 0,
        direct_h = lambda x, sid: 0,
        ask_h = lambda x, y, z: { 'value': random.choice(y['options']) },
        update_h = lambda x, y: 0
    )
    p.gc = gc 
    return p


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
        'location': 'None',
        'character': 'None',
        'modifiers': {}
    })

def test_setCharacter():
    p = player.Player('Max', 'socket_id')
    assert not p.character
    c = character.Character(
        name = "char_name",
        alleg = 1,
        max_hp = 10,
        win_cond = lambda: 5,
        win_cond_desc = "win_desc",
        special = lambda: 5,
        resource_id = "r_id"
    )
    p.setCharacter(c)
    assert p.character == c

def test_reveal():
    p = player.Player('Max', 'socket_id')
    assert p.state == 2
    p.reveal()
    assert p.state == 1

def test_drawCard():
    assert 1

def test_attack():
    assert 1

def test_defend():
    assert 1

def test_moveHP():
    p = init_player()
    assert p.hp == 0
    p.moveHP(-5)
    assert p.hp == 5
    p.moveHP(-50)
    assert p.hp == p.character.max_hp
    p.moveHP(100)
    assert p.hp == 0

def test_setHP():
    p = init_player()
    assert p.hp == 0
    p.setHP(5)
    assert p.hp == 5

def test_checkDeath():
    p = init_player() 
    p.checkDeath()
    assert p.state == 2
    p.hp = 20
    p.checkDeath()
    assert p.state == 0

def test_move():
    p = player.Player('Max', 'socket_id')
    assert not p.location
    a = area.Area(
        name = "area_name",
        desc = "area_desc",
        domain = [9],
        action = lambda: 5,
        resource_id = "r_id"
    )
    p.move(a)
    assert p.location == a
