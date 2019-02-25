import card, deck, character, area

# cli.py
# Provides a CLI to the game.
# For now -- run with python -i cli.py

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
        use = lambda: 0  # TODO
    ),
    card.Card(
        title = "Flare of Judgement",
        desc = "All characters except yourself receive 2 points of damage.",
        color = 0,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # TODO
    ),
    card.Card(
        title = "First Aid",
        desc = "Place a character's HP marker to 7 (You can choose yourself).",
        color = 0,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # TODO
    ),
    card.Card(
        title = "Holy Water of Healing",
        desc = "Heal 2 points of your damage.",
        color = 0,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # TODO
    ),
    card.Card(
        title = "Holy Water of Healing",
        desc = "Heal 2 points of your damage.",
        color = 0,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # TODO
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
        use = lambda: 0  # TODO
    ),
    card.Card(
        title = "Chainsaw",
        desc = "If your attack is successful, you give 1 point of extra damage.",
        color = 1, # 1 : BLACK
        holder = None,
        is_equip = True,
        force_use = False,
        use = lambda: 0  # TODO
    ),
    card.Card(
        title = "Rusted Broad Axe",
        desc = "If your attack is successful, you give 1 point of extra damage.",
        color = 1, # 1 : BLACK
        holder = None,
        is_equip = True,
        force_use = False,
        use = lambda: 0  # TODO
    ),
    card.Card(
        title = "Moody Goblin",
        desc = "You steal an equipment card from any character.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # TODO
    ),
    card.Card(
        title = "Moody Goblin",
        desc = "You steal an equipment card from any character.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # TODO
    ),
    card.Card(
        title = "Bloodthirsty Spider",
        desc = "You give 2 points of damage to any character and receive 2 points of damage yourself.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # TODO
    ),
    card.Card(
        title = "Vampire Bat",
        desc = "You give 2 points of damage to any character and heal 1 point of your own damage.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # TODO
    ),
    card.Card(
        title = "Vampire Bat",
        desc = "You give 2 points of damage to any character and heal 1 point of your own damage.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # TODO
    ),
    card.Card(
        title = "Vampire Bat",
        desc = "You give 2 points of damage to any character and heal 1 point of your own damage.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # TODO
    )
]

WHITE_DECK = deck.Deck(cards = WHITE_CARDS)
BLACK_DECK = deck.Deck(cards = BLACK_CARDS)
GREEN_DECK = deck.Deck(cards = [])


# Initialize characters
CHARACTERS = [
    character.Character(
        name = "Valkyrie",
        alleg = 0,  # Shadow
        max_hp = 13,
        win_cond = lambda: 0,  # TODO
        win_cond_desc = "All the Hunter characters are dead or 3 Neutral characters are dead",
        special = lambda: 0,  # TODO
        resource_id = "valkyrie"
    ),
    character.Character(
        name = "Vampire",
        alleg = 0,  # Shadow
        max_hp = 13,
        win_cond = lambda: 0,  # TODO
        win_cond_desc = "All the Hunter characters are dead or 3 Neutral characters are dead",
        special = lambda: 0,  # TODO
        resource_id = "vampire"
    ),
    character.Character(
        name = "Allie",
        alleg = 1,  # Neutral
        max_hp = 8,
        win_cond = lambda: 0,  # TODO
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

# Initialize areas
AREAS = [
    area.Area(
        name = "Hermit's Cabin",
        desc = "You may draw a Hermit Card.",
        domain = [2, 3],
        action = lambda gc, player: player.drawCard(gc.green_cards),
        resource_id = "hermits-cabin"
    ),
    area.Area(
        name = "Underworld Gate",
        desc = "You may draw a card from the stack of your choice.",
        domain = [4, 5],
        action = lambda gc, player: 0,  # TODO
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
        action = lambda gc, player: 0,  # TODO
        resource_id = "weird-woods"
    ),
    area.Area(
        name = "Erstwhile Altar",
        desc = "You may steal an equipment card from any player.",
        domain = [10],
        action = lambda gc, player: 0,  # TODO
        resource_id = "erstwhile-altar"
    )
]
