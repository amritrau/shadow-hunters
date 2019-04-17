import random

import game_context
import player
import elements

# helper functions

def color_format(str, args, gc):

    # get all elements by name
    ef = elements.ElementFactory()
    cards = [c.title for c in ef.WHITE_DECK.cards + ef.BLACK_DECK.cards + ef.GREEN_DECK.cards]
    shadows = [ch.name for ch in ef.CHARACTERS if ch.alleg == 0]
    hunters = [ch.name for ch in ef.CHARACTERS if ch.alleg == 2]
    neutrals = [ch.name for ch in ef.CHARACTERS if ch.alleg == 1]
    areas = [a.name for a in ef.AREAS]

    # assign colors
    colors = [elements.TEXT_COLORS['s']]
    for n in args:
        if gc:
            p = [p for p in gc.players if p.user_id == n]
        if isinstance(n, int):
            colors.append(elements.TEXT_COLORS['number'])
        elif n in cards:
            colors.append(elements.TEXT_COLORS['card'])
        elif n in shadows:
            colors.append(elements.TEXT_COLORS['shadow'])
        elif n in hunters:
            colors.append(elements.TEXT_COLORS['hunter'])
        elif n in neutrals:
            colors.append(elements.TEXT_COLORS['neutral'])
        elif n in areas:
            colors.append(elements.TEXT_COLORS['area'])
        elif gc and p:
            colors.append(p[0].color)
        else:
            colors.append(elements.TEXT_COLORS['s'])
        colors.append(elements.TEXT_COLORS['s'])

    # assign strings
    args += ['']
    strings = sum([[s, args.pop(0)] for s in str.split('{}')], [])[:-1]

    # return tuple of strings and colors
    return (strings, colors)

def answer_sequence(answers):
    '''create an ask function that will return a specific sequence of answers'''

    def ask_function(x, y, z):
        val = ask_function.sequence.pop(0)
        assert (val in y['options'])
        return { 'value': val }
    ask_function.sequence = answers
    return ask_function

def fresh_gc_ef(ask_function = lambda x, y, z: {'value': random.choice(y['options'])}):
    '''return a fresh game and element factory with the specified ask function'''

    def dummy_tell(data, client=None):
        return 0

    def dummy_show(data, client=None):
        return 0

    player_names = ['Amrit', 'Max', 'Gia', 'Joanna', 'Vishal']
    players = [player.Player(user_id, 'unused', ask_function, True) for user_id in player_names]
    ef = elements.ElementFactory()
    gc = game_context.GameContext(
        players = players,
        characters = ef.CHARACTERS,
        black_cards = ef.BLACK_DECK,
        white_cards = ef.WHITE_DECK,
        green_cards = ef.GREEN_DECK,
        areas = ef.AREAS,
        tell_h = dummy_tell,
        show_h = dummy_show,
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
