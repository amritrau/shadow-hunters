import pytest
import random

import game_context
import player
from tests import helpers

# test_win_conds.py
# Tests the win conditions of each character

def test_hunters_win():

    # Check that hunters don't win until shadows are dead
    gc, ef = helpers.fresh_gc_ef()
    h = helpers.get_a_hunter(gc)
    assert not h.character.win_cond(gc, h)
    for p in gc.players:
        if p != h:
            p.setDamage(14)
    assert h.character.win_cond(gc, h)

def test_shadows_win():

    # Check that shadows don't win until hunters are dead
    gc, ef = helpers.fresh_gc_ef()
    s = helpers.get_a_shadow(gc)
    assert not s.character.win_cond(gc, s)
    for p in gc.players:
        if p != s:
            p.setDamage(14)
    assert s.character.win_cond(gc, s)

    # TODO: Check that shadows win if three neutrals are dead
    # Requires support for 8-player games

def test_allie_win():

    # Keep creating games until we find Allie
    allie = None
    gc = None
    ef = None
    while not allie:
        gc, ef = helpers.fresh_gc_ef()
        for p in gc.players:
            if p.character.name == "Allie":
                allie = p
    
    # Check that Allie hasn't won if the game isn't over
    assert not allie.character.win_cond(gc, allie)

    # Check that Allie wins if the game is over and she is alive
    gc.game_over = True
    assert allie.character.win_cond(gc, allie)

    # Check that Allie doesn't win if she's dead
    allie.setDamage(14)
    assert not allie.character.win_cond(gc, allie)

