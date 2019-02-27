import card, deck, character, area

# cli.py
# Provides a CLI to the game.
# For now -- run with python -i cli.py

ALLEGIANCE_MAP = {
    0: "Shadow",
    1: "Neutral",
    2: "Hunter"
}

CARD_COLOR_MAP = {
    0: "White",
    1: "Black",
    2: "Green"
}

#####
# TODO For the following functions, insert descriptive tell_h()'s
def use_bloodthirsty_spider(args):
    target = args['self'].gc.ask_h('select', {'options': [t.user_id for t in args['self'].gc.getLivePlayers() if t != args['self']]}, args['self'].user_id)['value']
    args['self'].gc.update_h('select', {})
    [p for p in args['self'].gc.getLivePlayers() if p.user_id == target][0].moveHP(-2)
    args['self'].moveHP(-2)

def use_vampire_bat(args):
    target = args['self'].gc.ask_h('select', {'options': [t.user_id for t in args['self'].gc.getLivePlayers() if t != args['self']]}, args['self'].user_id)['value']
    args['self'].gc.update_h('select', {})
    [p for p in args['self'].gc.getLivePlayers() if p.user_id == target][0].moveHP(-2)
    args['self'].moveHP(1)

def use_first_aid(args):
    target = args['self'].gc.ask_h('select', {'options': [t.user_id for t in args['self'].gc.getLivePlayers()]}, args['self'].user_id)['value']
    args['self'].gc.update_h('select', {})
    [p for p in args['self'].gc.getLivePlayers() if p.user_id == target][0].setHP(7)

def use_moody_goblin(args):
    data = {'options': [p.user_id for p in args['self'].gc.getLivePlayers()]}
    target = args['self'].gc.ask_h('select', data, args['self'].user_id)['value']
    args['self'].gc.update_h('select', {})
    target_Player = [p for p in args['self'].gc.getLivePlayers() if p.user_id == target][0]

    data = {'options': [str(eq) for eq in target_Player.equipment]}
    equip = args['self'].gc.ask_h('select', data, args['self'].user_id)['value']
    args['self'].gc.update_h('select', {})
    equip_Equipment = [eq for eq in target_Player.equipment if str(eq) == equip][0]

    i = target_Player.equipment.index(equip_Equipment)
    equip_Equipment = target_Player.equipment.pop(i)
    args['self'].equipment.append(equip_Equipment)
    equip_Equipment.holder = player
    args['self'].gc.tell_h("{} stole {}'s {}!".format(player.user_id, target_Player.user_id, equip_Equipment.name))

##################



# TODO Hermit cards, Characters, and Areas

# Initialize cards and decks
WHITE_CARDS = [
    card.Card(
        title = "Holy Robe",
        desc = "Your attacks do 1 less damage and the amount of damage you receive from attacks is reduced by 1 point.",
        color = 0, # 0 : WHITE
        holder = None,
        is_equip = True,
        force_use = False,
        use = lambda is_attack, amt: amt - 1  # applies to both attack and defend
    ),
    card.Card(
        title = "Flare of Judgement",
        desc = "All characters except yourself receive 2 points of damage.",
        color = 0,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda args: [p.moveHP(-2) for p in args['self'].gc.getLivePlayers() if p != args['self']]
    ),
    card.Card(
        title = "First Aid",
        desc = "Place a character's HP marker to 7 (You can choose yourself).",
        color = 0,
        holder = None,
        is_equip = False,
        force_use = True,
        use = use_first_aid
    ),
    card.Card(
        title = "Holy Water of Healing",
        desc = "Heal 2 points of your damage.",
        color = 0,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda args: args['self'].moveHP(2)
    ),
    card.Card(
        title = "Holy Water of Healing",
        desc = "Heal 2 points of your damage.",
        color = 0,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda args: args['self'].moveHP(2)
    )
]

BLACK_CARDS = [
    card.Card(
        title = "Butcher Knife",
        desc = "If your attack is successful, you give 1 point of extra damage.",
        color = 1, # 1 : BLACK
        holder = None,
        is_equip = True,
        force_use = False,
        use = lambda is_attack, amt: amt + is_attack  # if we're attacking give 1 point extra
    ),
    card.Card(
        title = "Chainsaw",
        desc = "If your attack is successful, you give 1 point of extra damage.",
        color = 1, # 1 : BLACK
        holder = None,
        is_equip = True,
        force_use = False,
        use = lambda is_attack, amt: amt + is_attack
    ),
    card.Card(
        title = "Rusted Broad Axe",
        desc = "If your attack is successful, you give 1 point of extra damage.",
        color = 1, # 1 : BLACK
        holder = None,
        is_equip = True,
        force_use = False,
        use = lambda is_attack, amt: amt + is_attack
    ),
    card.Card(
        title = "Moody Goblin",
        desc = "You steal an equipment card from any character.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = use_moody_goblin
    ),
    card.Card(
        title = "Moody Goblin",
        desc = "You steal an equipment card from any character.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = use_moody_goblin
    ),
    card.Card(
        title = "Bloodthirsty Spider",
        desc = "You give 2 points of damage to any character and receive 2 points of damage yourself.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = use_bloodthirsty_spider
    ),
    card.Card(
        title = "Vampire Bat",
        desc = "You give 2 points of damage to any character and heal 1 point of your own damage.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = use_vampire_bat
    ),
    card.Card(
        title = "Vampire Bat",
        desc = "You give 2 points of damage to any character and heal 1 point of your own damage.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = use_vampire_bat
    ),
    card.Card(
        title = "Vampire Bat",
        desc = "You give 2 points of damage to any character and heal 1 point of your own damage.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = use_vampire_bat
    )
]

WHITE_DECK = deck.Deck(cards = WHITE_CARDS)
BLACK_DECK = deck.Deck(cards = BLACK_CARDS)
GREEN_DECK = deck.Deck(cards = [])


# Initialize characters
def shadow_win_cond(gc, player):
    no_living_hunters = len([p for p in gc.getLivePlayers() if p.character.alleg == 2]) == 0
    neutrals_dead_3 = len([p for p in gc.getDeadPlayers() if p.character.alleg == 1]) >= 3
    return no_living_hunters or neutrals_dead_3

def hunter_win_cond(gc, player):
    no_living_shadows = len([p for p in gc.getLivePlayers() if p.character.alleg == 0]) == 0
    return no_living_shadows

def allie_win_cond(gc, player):
    return (player in gc.getLivePlayers()) and gc.game_over

CHARACTERS = [
    character.Character(
        name = "Valkyrie",
        alleg = 0,  # Shadow
        max_hp = 13,
        win_cond = shadow_win_cond,
        win_cond_desc = "All the Hunter characters are dead or 3 Neutral characters are dead",
        special = lambda: 0,  # TODO
        resource_id = "valkyrie"
    ),
    character.Character(
        name = "Vampire",
        alleg = 0,  # Shadow
        max_hp = 13,
        win_cond = shadow_win_cond,
        win_cond_desc = "All the Hunter characters are dead or 3 Neutral characters are dead",
        special = lambda: 0,  # TODO
        resource_id = "vampire"
    ),
    character.Character(
        name = "Allie",
        alleg = 1,  # Neutral
        max_hp = 8,
        win_cond = allie_win_cond,
        win_cond_desc = "You're not dead when the game is over",
        special = lambda: 0,  # TODO
        resource_id = "allie"
    ),
    character.Character(
        name = "George",
        alleg = 2,  # Hunter
        max_hp = 14,
        win_cond = lambda: 0,  # TODO
        win_cond_desc = "All the Shadow characters are dead",
        special = lambda: 0,  # TODO
        resource_id = "george"
    ),
    character.Character(
        name = "Fu-ka",
        alleg = 2,  # Hunter
        max_hp = 12,
        win_cond = lambda: 0,  # TODO
        win_cond_desc = "All the Shadow characters are dead",
        special = lambda: 0,  # TODO
        resource_id = "fu-ka"
    )
]

##########
# TODO For the following functions, insert descriptive tell_h()'s
def underworld_gate_action(gc, player):
    data = {'options': ["Draw White Card", "Draw Black Card", "Draw Green Card"]}
    answer = gc.ask_h('select', data, player.user_id)['value']
    gc.update_h('select', {})
    if answer == "Draw White Card":
        player.drawCard(gc.white_cards)
    elif answer == "Draw Black Card":
        player.drawCard(gc.black_cards)
    else:
        player.drawCard(gc.green_cards)

def weird_woods_action(gc, player):
    data = {'options': [p.user_id for p in gc.getLivePlayers()]}
    target = gc.ask_h('select', data, player.user_id)['value']
    gc.update_h('select', {})
    target_Player = [p for p in gc.getLivePlayers() if p.user_id == target][0]

    data = {'options': ["Heal 1 HP", "Damage 2 HP"]}
    amount = gc.ask_h('select', data, player.user_id)['value']
    gc.update_h('select', {})
    if amount == "Heal 1 HP":
        target_Player.moveHP(1)
    else:
        target_Player.moveHP(-2)

def erstwhile_altar_action(gc, player):
    # TODO Only show players with items
    # TODO Handle case: nobody has any items
    data = {'options': [p.user_id for p in gc.getLivePlayers()]}
    target = gc.ask_h('select', data, player.user_id)['value']
    gc.update_h('select', {})
    target_Player = [p for p in gc.getLivePlayers() if p.user_id == target][0]

    data = {'options': [str(eq) for eq in target_Player.equipment]}
    equip = gc.ask_h('select', data, player.user_id)['value']
    gc.update_h('select', {})
    equip_Equipment = [eq for eq in target_Player.equipment if str(eq) == equip][0]

    i = target_Player.equipment.index(equip_Equipment)
    equip_Equipment = target_Player.equipment.pop(i)
    player.equipment.append(equip_Equipment)
    equip_Equipment.holder = player
    gc.tell_h("{} stole {}'s {}!".format(player.user_id, target_Player.user_id, equip_Equipment.name))

#########

# Initialize areas
AREAS = [
    area.Area(
        name = "Hermit's Cabin",
        desc = "You may draw a Hermit Card.",
        domain = [2, 3],
        # TODO uncomment below once green cards are implemented
        action = lambda gc, player: 0, # player.drawCard(gc.green_cards),
        resource_id = "hermits-cabin"
    ),
    area.Area(
        name = "Underworld Gate",
        desc = "You may draw a card from the stack of your choice.",
        domain = [4, 5],
        action = underworld_gate_action,
        resource_id = "underworld-gate"
    ),
    area.Area(
        name = "Church",
        desc = "You may draw a White Card.",
        domain = [6],
        action = lambda gc, player: player.drawCard(gc.white_cards),
        resource_id = "church"
    ),
    area.Area(
        name = "Cemetery",
        desc = "You may draw a Black Card.",
        domain = [8],
        action = lambda gc, player: player.drawCard(gc.black_cards),
        resource_id = "cemetery"
    ),
    area.Area(
        name = "Weird Woods",
        desc = "You may either give 2 damage to any player or heal 1 damage of any player.",
        domain = [9],
        action = weird_woods_action,
        resource_id = "weird-woods"
    ),
    area.Area(
        name = "Erstwhile Altar",
        desc = "You may steal an equipment card from any player.",
        domain = [10],
        action = erstwhile_altar_action,  # TODO
        resource_id = "erstwhile-altar"
    )
]
