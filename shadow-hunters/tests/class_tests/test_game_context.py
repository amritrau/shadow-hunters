import pytest
import random

import game_context
import player
import cli

# test_game_context.py
# Tests for the GameContext object

# helper function to return a fresh game context
def fresh_gc():
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
    return gc

def test_fields():
    
    # test initialization
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
        tell_h = lambda x: 5,
        direct_h = lambda x, sid: 5,
        ask_h = lambda x, y, z: { 'value': random.choice(y['options']) },
        update_h = lambda x, y: 5
    )
 
    # test fields
    assert gc.players == players
    assert gc.characters == ef.CHARACTERS
    assert gc.black_cards == ef.BLACK_DECK
    assert gc.white_cards == ef.WHITE_DECK
    assert gc.green_cards == ef.GREEN_DECK
    assert gc.tell_h(0) == 5
    assert gc.direct_h(0, 0) == 5
    assert gc.ask_h(0, { 'options': ['test'] }, 0) == { 'value': 'test' }
    assert gc.update_h(0, 0) == 5
    assert not gc.modifiers
    assert gc.die4.n_sides == 4
    assert gc.die6.n_sides == 6
    for p in players:
        assert p.gc == gc
        assert p.character is not None
    for a in ef.AREAS:
        assert a.zone is not None
    assert len(gc.zones) == 3
    assert [len(z.areas) == 2 for z in gc.zones]

    # test dump
    public, private = gc.dump()
    assert private == {p.socket_id: p.dump() for p in gc.players}
    assert public['zones'] == [z.dump() for z in gc.zones]    

def test_getLivePlayers():
    gc = fresh_gc()
    assert gc.getLivePlayers() == gc.players
    gc.players[0].setHP(14)
    assert gc.getLivePlayers() == gc.players[1:]

def test_getDeadPlayers():
    gc = fresh_gc()
    assert not gc.getDeadPlayers()
    gc.players[0].setHP(14)
    assert gc.getDeadPlayers() == [gc.players[0]]

def test_checkWinConditions():
    gc = fresh_gc()
    assert not gc.checkWinConditions()
    gc.play()
    assert gc.checkWinConditions()

    gc = fresh_gc()
    for p in gc.players:
        if p.character.alleg != 2:
            p.setHP(14)
    assert all([p.character.alleg == 2 for p in gc.checkWinConditions()])

    gc = fresh_gc()
    for p in gc.players:
        if p.character.alleg != 0:
            p.setHP(14)
    assert all([p.character.alleg == 0 for p in gc.checkWinConditions()])

def test_play():
    gc = fresh_gc()
    winners = gc.play()
    assert winners
