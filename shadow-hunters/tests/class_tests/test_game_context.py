import pytest

from constants import Alleg
from helpers import fresh_gc_ef
import random

# test_game_context.py
# Tests for the GameContext object


def test_fields():

    # Multiple runs to get many different shuffles
    for _ in range(100):

        # test initialization
        n_players = random.randint(4, 8)
        gc, ef = fresh_gc_ef(n_players)

        # test fields
        assert len(gc.players) == n_players
        assert gc.black_cards == ef.BLACK_DECK
        assert gc.white_cards == ef.WHITE_DECK
        assert gc.green_cards == ef.GREEN_DECK
        assert not gc.modifiers
        assert gc.die4.n_sides == 4
        assert gc.die6.n_sides == 6
        for p in gc.players:
            assert p.gc == gc
            assert p.character is not None
        for a in ef.AREAS:
            assert a.zone is not None
        assert len(gc.zones) == 3
        assert [len(z.areas) == 2 for z in gc.zones]

    # test dump
    public, private = gc.dump()
    # assert private == [p.dump() for p in gc.players]
    # assert public['zones'] == [z.dump() for z in gc.zones]


def test_getLivePlayers():
    gc, ef = fresh_gc_ef()

    # Check that all players are initially alive
    assert gc.getLivePlayers() == gc.players

    # Check that dead players are not included in alive players
    gc.players[0].setDamage(14, gc.players[1])
    assert gc.getLivePlayers() == gc.players[1:]


def test_getDeadPlayers():
    gc, ef = fresh_gc_ef()

    # Check that no players are initially dead
    assert not gc.getDeadPlayers()

    # Check that dead players are properly included
    gc.players[0].setDamage(14, gc.players[1])
    assert gc.getDeadPlayers() == [gc.players[0]]


def test_checkWinConditions():
    gc, ef = fresh_gc_ef()

    # Check that no one has initially won
    assert not gc.checkWinConditions()

    # Check that someone wins when a game is over
    gc.play()
    assert gc.checkWinConditions()

    # Check that hunters win when everyone else is dead
    gc, ef = fresh_gc_ef()
    for p in gc.players:
        if p.character.alleg == Alleg.Shadow:
            p.setDamage(14, p)
    assert [p for p in gc.checkWinConditions()
            if p.character.alleg == Alleg.Hunter]

    # Check that shadows win when everyone else is dead
    gc, ef = fresh_gc_ef()
    for p in gc.players:
        if p.character.alleg == Alleg.Hunter:
            p.setDamage(14, p)
    assert [p for p in gc.checkWinConditions()
            if p.character.alleg == Alleg.Shadow]


def test_play():
    gc, ef = fresh_gc_ef()

    # Check that a game plays to completion
    gc.play()
    assert 1
