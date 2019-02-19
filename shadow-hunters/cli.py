import card, deck

# cli.py
# Provides a CLI to the game.
# For now -- run with python -i cli.py

# Initialize cards and decks
WHITE_CARDS = [
    card.Card(
        title = "Holy Robe",
        desc = "Your attacks do 1 less damage and the amount of damage you receive from attacks is reduced by 1 point.",
        color = 0, # 0 : WHITE
        holder = None,
        is_equip = True,
        force_use = False,
        use = lambda: 0  # placeholder
    ),
    card.Card(
        title = "Flare of Judgement",
        desc = "All characters except yourself receive 2 points of damage.",
        color = 0,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # placeholder
    ),
    card.Card(
        title = "First Aid",
        desc = "Place a character's HP marker to 7 (You can choose yourself).",
        color = 0,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # placeholder
    ),
    card.Card(
        title = "Holy Water of Healing",
        desc = "Heal 2 points of your damage.",
        color = 0,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # placeholder
    ),
    card.Card(
        title = "Holy Water of Healing",
        desc = "Heal 2 points of your damage.",
        color = 0,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # placeholder
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
        use = lambda: 0  # placeholder
    ),
    card.Card(
        title = "Chainsaw",
        desc = "If your attack is successful, you give 1 point of extra damage.",
        color = 1, # 1 : BLACK
        holder = None,
        is_equip = True,
        force_use = False,
        use = lambda: 0  # placeholder
    ),
    card.Card(
        title = "Rusted Broad Axe",
        desc = "If your attack is successful, you give 1 point of extra damage.",
        color = 1, # 1 : BLACK
        holder = None,
        is_equip = True,
        force_use = False,
        use = lambda: 0  # placeholder
    ),
    card.Card(
        title = "Moody Goblin",
        desc = "You steal an equipment card from any character.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # placeholder
    ),
    card.Card(
        title = "Moody Goblin",
        desc = "You steal an equipment card from any character.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # placeholder
    ),
    card.Card(
        title = "Bloodthirsty Spider",
        desc = "You give 2 points of damage to any character and receive 2 points of damage yourself.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # placeholder
    ),
    card.Card(
        title = "Vampire Bat",
        desc = "You give 2 points of damage to any character and heal 1 point of your own damage.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # placeholder
    ),
    card.Card(
        title = "Vampire Bat",
        desc = "You give 2 points of damage to any character and heal 1 point of your own damage.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # placeholder
    ),
    card.Card(
        title = "Vampire Bat",
        desc = "You give 2 points of damage to any character and heal 1 point of your own damage.",
        color = 1,
        holder = None,
        is_equip = False,
        force_use = True,
        use = lambda: 0 # placeholder
    )
]

WHITE_DECK = deck.Deck(cards = WHITE_CARDS)
BLACK_DECK = deck.Deck(cards = BLACK_CARDS)
