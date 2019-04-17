import pytest
import random

import game_context
import player
import helpers

# test_win_conds.py
# Tests the win conditions of each character

def test_hunters_win():

    # Check that hunters don't win until shadows are dead
    gc, ef = helpers.fresh_gc_ef()
    h = helpers.get_a_hunter(gc)
    assert not h.character.win_cond(gc, h)
    for p in gc.players:
        if p != h:
            p.setDamage(14, p)
    assert h.character.win_cond(gc, h)

def test_shadows_win():

    # Check that shadows don't win until hunters are dead
    gc, ef = helpers.fresh_gc_ef()
    s = helpers.get_a_shadow(gc)
    assert not s.character.win_cond(gc, s)
    for p in gc.players:
        if p != s:
            p.setDamage(14, p)
    assert s.character.win_cond(gc, s)

    # Check that shadows win if three neutrals are dead
    gc, ef = helpers.fresh_gc_ef(7)
    s = helpers.get_a_shadow(gc)
    for p in gc.players:
        if p.character.alleg == 1:
            p.setDamage(14, p)
    assert s.character.win_cond(gc, s)

def test_allie_win():

    # Get a game containing Allie
    gc, ef, p = helpers.get_game_with_character("Allie")

    # Check that Allie hasn't won if the game isn't over
    assert not p.character.win_cond(gc, p)

    # Check that Allie wins if the game is over and she is alive
    gc.game_over = True
    assert p.character.win_cond(gc, p)

    # Check that Allie doesn't win if she's dead
    p.setDamage(14, p)
    assert not p.character.win_cond(gc, p)

def test_bob_win():

    # Get a game containing Bob
    gc, ef, p = helpers.get_game_with_character("Bob")

    # Check that Bob hasn't won initially, or with 4 equips
    assert not p.character.win_cond(gc, p)
    p.equipment = ['dummy_equipment'] * 4
    assert not p.character.win_cond(gc, p)

    # Check that Bob wins if we give him 5 equipment cards, or more
    p.equipment = ['dummy_equipment'] * 5
    assert p.character.win_cond(gc, p)
    p.equipment = ['dummy_equipment'] * 10
    assert p.character.win_cond(gc, p)

def test_catherine_win():

    # Get a game containing Catherine
    gc, ef, p = helpers.get_game_with_character("Catherine")

    # Check that Catherine hasn't won initially
    assert not p.character.win_cond(gc, p)

    # Check that Catherine wins if she dies first
    p.setDamage(14, p)
    assert p.character.win_cond(gc, p)

    # Check that Catherine does not win if she dies second
    gc, ef, p = helpers.get_game_with_character("Catherine")
    h = helpers.get_a_hunter(gc)
    h.setDamage(14, h)
    p.setDamage(14, p)
    assert not p.character.win_cond(gc, p)

    # Check that Catherine wins if she's in the last two standing
    gc, ef, p = helpers.get_game_with_character("Catherine", n_players=6)
    for pl in gc.players:
        if pl.character.alleg != 1:
            pl.setDamage(14, pl)
    assert p.character.win_cond(gc, p)
