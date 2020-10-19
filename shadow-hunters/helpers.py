from game_context import GameContext
from elements import ElementFactory
from player import Player

import constants as C
import random

# helper functions frontend communication


def color_format(str, args, gc):

    # get all elements by name
    ef = ElementFactory()
    all_cards = ef.WHITE_DECK.cards + ef.BLACK_DECK.cards + ef.GREEN_DECK.cards
    cards = [c.title for c in all_cards]
    shadows = [c.name for c in ef.CHARACTERS if c.alleg == C.Alleg.Shadow]
    hunters = [c.name for c in ef.CHARACTERS if c.alleg == C.Alleg.Hunter]
    neutrals = [c.name for c in ef.CHARACTERS if c.alleg == C.Alleg.Neutral]
    areas = [a.name for a in ef.AREAS]

    # assign colors
    colors = [C.TEXT_COLORS['server']]
    for n in args:
        if gc:
            p = [p for p in gc.players if p.user_id == n]
        if isinstance(n, int):
            colors.append(C.TEXT_COLORS['number'])
        elif n in cards:
            card_color = C.CARD_COLOR_MAP[(
                [c for c in all_cards if c.title == n][0]).color]
            colors.append(C.TEXT_COLORS[card_color])
        elif n == 'a Hermit Card':
            colors.append(C.TEXT_COLORS['Green'])
        elif n in shadows or n == 'Shadow':
            colors.append(C.TEXT_COLORS['shadow'])
        elif n in hunters or n == 'Hunter':
            colors.append(C.TEXT_COLORS['hunter'])
        elif n in neutrals or n == 'Neutral':
            colors.append(C.TEXT_COLORS['neutral'])
        elif n in areas:
            colors.append(C.TEXT_COLORS[n])
        elif gc and p:
            colors.append(p[0].color)
        else:
            colors.append(C.TEXT_COLORS['server'])
        colors.append(C.TEXT_COLORS['server'])

    # assign strings
    args += ['']
    strings = sum([[s, args.pop(0)] for s in str.split('{}')], [])[:-1]

    # return tuple of strings and colors
    return (strings, colors)

# Helper functions for data retrieval


def get_room_id(rooms, sid):
    candidates = [r for r in rooms.keys() if sid in rooms[r]
                  ['connections'].keys()]
    if not candidates:
        return None
    else:
        return candidates[0]


def get_reserved_words():
    ef = ElementFactory()
    cards = ef.WHITE_DECK.cards + ef.BLACK_DECK.cards + ef.GREEN_DECK.cards
    reserved = [c.title for c in cards]
    reserved += [ch.name for ch in ef.CHARACTERS]
    reserved += [a.name for a in ef.AREAS]
    reserved += ["Shadow", "Hunter", "Neutral", "Decline"]
    return reserved


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


def get_a_hunter(gc):
    return [p for p in gc.players if p.character.alleg == C.Alleg.Hunter][0]


def get_a_shadow(gc):
    return [p for p in gc.players if p.character.alleg == C.Alleg.Shadow][0]


def get_a_neutral(gc):
    return [p for p in gc.players if p.character.alleg == C.Alleg.Neutral][0]

# Helper functions for unit testing


def answer_sequence(answers):
    def ask_function(x, y, z):
        val = ask_function.sequence.pop(0)
        assert (val in y['options'])
        return {'value': val}
    ask_function.sequence = answers
    return ask_function


def fresh_gc_ef(n_players=random.randint(4, 8)):
    players = [Player("CPU_{}".format(
        i), 'unused', 'unused', True) for i in range(1, n_players + 1)]
    ef = ElementFactory()

    gc = GameContext(
        players=players,
        characters=ef.CHARACTERS,
        black_cards=ef.BLACK_DECK,
        white_cards=ef.WHITE_DECK,
        green_cards=ef.GREEN_DECK,
        areas=ef.AREAS,
        ask_h=lambda x, y, z: {'value': random.choice(y['options'])},
        tell_h=lambda x, y, *z: 0,
        show_h=lambda x, *y: 0,
        update_h=lambda: 0
    )
    return (gc, ef)


def get_game_with_character(name, n_players=random.randint(5, 8)):
    char = None
    gc = None
    ef = None
    while not char:
        gc, ef = fresh_gc_ef(n_players=n_players)
        for p in gc.players:
            if p.character.name == name:
                char = p
    return (gc, ef, char)
