import random

import game_context
import player
import cli

# helper functions to create a rigged game context for unit testing

def answer_sequence(answers):
    '''create an ask function that will return a specific sequence of answers'''

    def ask_function(x, y, z):
        return { 'value': ask_function.sequence.pop(0) }
    ask_function.sequence = answers
    return ask_function

def fresh_gc_ef(ask_function = lambda x, y, z: { 'value': random.choice(y['options']) }):
    '''return a fresh game and element factory with the specified ask function'''

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
        ask_h = ask_function,
        update_h = lambda: 0
    )
    return (gc, ef)

def get_a_hunter(gc):
    for p in gc.players:
        if p.character.alleg == 2:
            return p

def get_a_shadow(gc):
    for p in gc.players:
        if p.character.alleg == 0:
            return p

def get_a_neutral(gc):
    for p in gc.players:
        if p.character.alleg == 1:
            return p

def get_card_by_title(ef, title):

    # search white deck
    for c in ef.WHITE_DECK.cards:
        if c.title == title:
            return c

    # search black deck
    for c in ef.BLACK_DECK.cards:
        if c.title == title:
            return c

    # search green deck
    for c in ef.GREEN_DECK.cards:
        if c.title == title:
            return c
