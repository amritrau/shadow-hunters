from tests import helpers
import pytest
import random

import game_context
import player
import elements

# test_game_context.py
# Tests for the GameContext object

def test_fields():

    # test initialization
    player_names = ['Amrit', 'Max', 'Gia', 'Joanna', 'Vishal']
    players = [player.Player(user_id, 'unused', lambda x, y, z: { 'value': random.choice(y['options']) }, True) for user_id in player_names]
    ef = elements.ElementFactory()
    gc = game_context.GameContext(
        players = players,
        characters = ef.CHARACTERS,
        black_cards = ef.BLACK_DECK,
        white_cards = ef.WHITE_DECK,
        green_cards = ef.GREEN_DECK,
        areas = ef.AREAS,
        tell_h = lambda x: 5,
        show_h = lambda x: 4,
        update_h = lambda: 3
    )

    # test fields
    assert gc.players == players
    assert gc.characters == ef.CHARACTERS
    assert gc.black_cards == ef.BLACK_DECK
    assert gc.white_cards == ef.WHITE_DECK
    assert gc.green_cards == ef.GREEN_DECK
    assert gc.tell_h(0) == 5
    assert gc.show_h(0) == 4
    assert gc.update_h() == 3
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
    assert private == [p.dump() for p in gc.players]
    assert public['zones'] == [z.dump() for z in gc.zones]

def test_getLivePlayers():
    gc, ef = helpers.fresh_gc_ef()

    # Check that all players are initially alive
    assert gc.getLivePlayers() == gc.players

    # Check that dead players are not included in alive players
    gc.players[0].setDamage(14, gc.players[1])
    assert gc.getLivePlayers() == gc.players[1:]

def test_getDeadPlayers():
    gc, ef = helpers.fresh_gc_ef()

    # Check that no players are initially dead
    assert not gc.getDeadPlayers()

    # Check that dead players are properly included
    gc.players[0].setDamage(14, gc.players[1])
    assert gc.getDeadPlayers() == [gc.players[0]]

def test_checkWinConditions():
    gc, ef = helpers.fresh_gc_ef()

    # Check that no one has initially won
    assert not gc.checkWinConditions()

    # Check that someone wins when a game is over
    gc.play()
    assert gc.checkWinConditions()

    # Check that hunters win when everyone else is dead
    gc, ef = helpers.fresh_gc_ef()
    for p in gc.players:
        if p.character.alleg != 2:
            p.setDamage(14, p)
    assert len([p for p in gc.checkWinConditions()]) != 0 and all([p.character.alleg == 2 for p in gc.checkWinConditions()])

    # Check that shadows win when everyone else is dead
    gc, ef = helpers.fresh_gc_ef()
    for p in gc.players:
        if p.character.alleg != 0:
            p.setDamage(14, p)
    assert len([p for p in gc.checkWinConditions()]) != 0 and all([p.character.alleg == 0 for p in gc.checkWinConditions()])

def test_play():
    gc, ef = helpers.fresh_gc_ef()

    # Check that a game plays to completion
    gc.play()
