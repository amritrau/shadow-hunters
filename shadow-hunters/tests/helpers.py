import random

import game_context
import player
import elements

# helper functions to create a rigged game context for unit testing

def answer_sequence(answers):
    '''create an ask function that will return a specific sequence of answers'''

    def ask_function(x, y, z):
        val = ask_function.sequence.pop(0)
        assert (val in y['options'])
        return { 'value': val }
    ask_function.sequence = answers
    return ask_function

def fresh_gc_ef(ask_function = lambda x, y, z: { 'value': random.choice(y['options']) }):
    '''return a fresh game and element factory with the specified ask function'''

    player_names = ['Amrit', 'Max', 'Gia', 'Joanna', 'Vishal']
    players = [player.Player(user_id, socket_id='unused') for user_id in player_names]
    ef = elements.ElementFactory()
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
    return [p for p in gc.players if p.character.alleg == 2][0]

def get_a_shadow(gc):
    return [p for p in gc.players if p.character.alleg == 0][0]

def get_a_neutral(gc):
    return [p for p in gc.players if p.character.alleg == 1][0]

def get_card_by_title(ef, title):
    all_cards = ef.WHITE_DECK.cards + ef.BLACK_DECK.cards + ef.GREEN_DECK.cards
    return [c for c in all_cards if c.title == title][0]

def get_area_by_name(gc, name):
    for z in gc.zones:
        for a in z.areas:
            if a.name == name:
                return a

def get_character_by_name(ef, name):
    return [c for c in ef.CHARACTERS if c.name == name][0]
