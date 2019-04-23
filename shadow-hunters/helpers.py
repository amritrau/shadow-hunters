from game_context import GameContext
import player
import elements
import random

# helper functions frontend communication


def color_format(str, args, gc):
    # get all elements by name
    ef = elements.ElementFactory()
    all_cards = ef.WHITE_DECK.cards + ef.BLACK_DECK.cards + ef.GREEN_DECK.cards
    cards = [c.title for c in all_cards]
    shadows = [ch.name for ch in ef.CHARACTERS if ch.alleg == 0]
    hunters = [ch.name for ch in ef.CHARACTERS if ch.alleg == 2]
    neutrals = [ch.name for ch in ef.CHARACTERS if ch.alleg == 1]
    areas = [a.name for a in ef.AREAS]

    # assign colors
    colors = [elements.TEXT_COLORS['server']]
    for n in args:
        if gc:
            p = [p for p in gc.players if p.user_id == n]
        if isinstance(n, int):
            colors.append(elements.TEXT_COLORS['number'])
        elif n in cards:
            item = [c for c in all_cards if c.title == n][0]
            card_color = elements.CARD_COLOR_MAP[item.color]
            colors.append(elements.TEXT_COLORS[card_color])
        elif n == 'a Hermit Card':
            colors.append(elements.TEXT_COLORS['Green'])
        elif n in shadows or n == 'Shadow':
            colors.append(elements.TEXT_COLORS['shadow'])
        elif n in hunters or n == 'Hunter':
            colors.append(elements.TEXT_COLORS['hunter'])
        elif n in neutrals or n == 'Neutral':
            colors.append(elements.TEXT_COLORS['neutral'])
        elif n in areas:
            colors.append(elements.TEXT_COLORS[n])
        elif gc and p:
            colors.append(p[0].color)
        else:
            colors.append(elements.TEXT_COLORS['server'])
        colors.append(elements.TEXT_COLORS['server'])

    # assign strings
    args += ['']
    strings = sum([[s, args.pop(0)] for s in str.split('{}')], [])[:-1]

    # return tuple of strings and colors
    return (strings, colors)

# Helper functions for data retrieval


def get_room_id(rooms, sid):
    cands = [r for r in rooms.keys() if sid in rooms[r]['connections'].keys()]
    if not cands:
        return None
    else:
        return cands[0]


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
    return [p for p in gc.players if p.character.alleg == 2][0]


def get_a_shadow(gc):
    return [p for p in gc.players if p.character.alleg == 0][0]


def get_a_neutral(gc):
    return [p for p in gc.players if p.character.alleg == 1][0]

# Helper functions for unit testing


def answer_sequence(answers):
    def ask_function(x, y, z):
        val = ask_function.sequence.pop(0)
        assert (val in y['options'])
        return {'value': val}
    ask_function.sequence = answers
    return ask_function


def fresh_gc_ef(n_players=random.randint(4, 8)):
    rng = range(1, n_players + 1)
    players = [player.Player("CPU_{}".format(i), '', '', True) for i in rng]
    ef = elements.ElementFactory()

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
