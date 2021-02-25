import card
import deck
import character
import area
import single_use
import hermit
import win_conditions
import specials

from constants import Alleg, CardType

# elements.py
# Encodes all characters, win conditions, special abilities,
# game areas, decks, and cards in an element factory. Every
# game context is initialized with its own element factory.


class ElementFactory:
    """Make all elements needed for the game."""

    def __init__(self):

        # Initialize white cards
        white_cards = [
            card.Card(
                title="Mystic Compass",
                desc=("When you move, you may roll twice "
                      "and choose which result to use."),
                color=CardType.White,
                holder=None,
                is_equip=True,
                use=None
            ),
            card.Card(
                title="Talisman",
                desc=("You receive no damage from Black cards"
                      " 'Bloodthirsty Spider', 'Vampire Bat', or 'Dynamite'."),
                color=CardType.White,
                holder=None,
                is_equip=True,
                use=None
            ),
            card.Card(
                title="Fortune Brooch",
                desc=(
                    "You receive no damage from the area card"
                    " 'Weird Woods'. You can still be healed by it."),
                color=CardType.White,
                holder=None,
                is_equip=True,
                use=None
            ),
            card.Card(
                title="Silver Rosary",
                desc=("If you kill another character, "
                      "you take all of their equipment cards."),
                color=CardType.White,
                holder=None,
                is_equip=True,
                use=None
            ),
            card.Card(
                title="Spear of Longinus",
                desc=("If you are a Hunter who has revealed their identity and"
                      " your attack is successful, you give 2 points of extra"
                      " damage."),
                color=CardType.White,
                holder=None,
                is_equip=True,
                use=None
            ),
            card.Card(
                title="Advent",
                desc=("If you are a Hunter, you may reveal your identity. "
                      "If you do, or if you are already revealed,"
                      " you heal fully."),
                color=CardType.White,
                holder=None,
                is_equip=False,
                use=single_use.advent
            ),
            card.Card(
                title="Disenchant Mirror",
                desc=("If you are a Shadow, except for Unknown, "
                      "you must reveal your identity."),
                color=CardType.White,
                holder=None,
                is_equip=False,
                use=single_use.disenchant_mirror
            ),
            card.Card(
                title="Blessing",
                desc=("Pick a character other than yourself and roll the"
                      " 6-sided die. That character heals an amount of damage"
                      " equal to the die roll."),
                color=CardType.White,
                holder=None,
                is_equip=False,
                use=single_use.blessing
            ),
            card.Card(
                title="Chocolate",
                desc=("If you are Allie, Agnes, Emi, Ellen, Unknown,"
                      " or Ultra Soul, you may reveal your identity. "
                      "If you do, or if you are already revealed, "
                      "you heal fully."),
                color=CardType.White,
                holder=None,
                is_equip=False,
                use=single_use.chocolate
            ),
            card.Card(
                title="Concealed Knowledge",
                desc="When this turn is over, it will be your turn again.",
                color=CardType.White,
                holder=None,
                is_equip=False,
                use=single_use.concealed_knowledge
            ),
            card.Card(
                title="Guardian Angel",
                desc=("You take no damage from the direct attacks of "
                      "other characters until the start of your next turn."),
                color=CardType.White,
                holder=None,
                is_equip=False,
                use=single_use.guardian_angel
            ),
            card.Card(
                title="Holy Robe",
                desc=("Your attacks do 1 less damage and the amount of"
                      " damage you receive from attacks is reduced by"
                      " 1 point."),
                color=CardType.White,
                holder=None,
                is_equip=True,
                use=lambda is_attack, successful, amt: max(
                    0, amt - 1)  # applies to both attack and defend
            ),
            card.Card(
                title="Flare of Judgement",
                desc=("All characters except yourself"
                      " receive 2 points of damage."),
                color=CardType.White,
                holder=None,
                is_equip=False,
                use=single_use.judgement
            ),
            card.Card(
                title="First Aid",
                desc=("Place a character's damage marker to 7"
                      " (You can choose yourself)."),
                color=CardType.White,
                holder=None,
                is_equip=False,
                use=single_use.first_aid
            ),
            card.Card(
                title="Holy Water of Healing",
                desc="Heal 2 points of your damage.",
                color=CardType.White,
                holder=None,
                is_equip=False,
                use=single_use.holy_water
            ),
            card.Card(
                title="Holy Water of Healing",
                desc="Heal 2 points of your damage.",
                color=CardType.White,
                holder=None,
                is_equip=False,
                use=single_use.holy_water
            )
        ]

        # Initialize black cards
        black_cards = [
            card.Card(
                title="Cursed Sword Masamune",
                desc=(
                    "You must attack another character on your turn."
                    " This attack uses the 4-sided die."),
                color=CardType.Black,
                holder=None,
                is_equip=True,
                use=None
            ),
            card.Card(
                title="Machine Gun",
                desc=(
                    "Your attack will affect all characters in your"
                    " attack range (the dice are rolled only once)."),
                color=CardType.Black,
                holder=None,
                is_equip=True,
                use=None
            ),
            card.Card(
                title="Handgun",
                desc="All ranges but yours become your attack range.",
                color=CardType.Black,
                holder=None,
                is_equip=True,
                use=None
            ),
            card.Card(
                title="Butcher Knife",
                desc=("If your attack is successful, "
                      "you give 1 point of extra damage."),
                color=CardType.Black,
                holder=None,
                is_equip=True,
                use=lambda is_attack, successful, amt: amt +
                1 if (is_attack and successful) else amt
            ),
            card.Card(
                title="Chainsaw",
                desc=("If your attack is successful, "
                      "you give 1 point of extra damage."),
                color=CardType.Black,
                holder=None,
                is_equip=True,
                use=lambda is_attack, successful, amt: amt +
                1 if (is_attack and successful) else amt
            ),
            card.Card(
                title="Rusted Broad Axe",
                desc=("If your attack is successful, "
                      "you give 1 point of extra damage."),
                color=CardType.Black,
                holder=None,
                is_equip=True,
                use=lambda is_attack, successful, amt: amt +
                1 if (is_attack and successful) else amt
            ),
            card.Card(
                title="Moody Goblin",
                desc="You steal an equipment card from any character.",
                color=CardType.Black,
                holder=None,
                is_equip=False,
                use=single_use.moody_goblin
            ),
            card.Card(
                title="Moody Goblin",
                desc="You steal an equipment card from any character.",
                color=CardType.Black,
                holder=None,
                is_equip=False,
                use=single_use.moody_goblin
            ),
            card.Card(
                title="Bloodthirsty Spider",
                desc=("You give 2 points of damage to any character"
                      " and receive 2 points of damage yourself."),
                color=CardType.Black,
                holder=None,
                is_equip=False,
                use=single_use.bloodthirsty_spider
            ),
            card.Card(
                title="Vampire Bat",
                desc=("You give 2 points of damage to any character"
                      " and heal 1 point of your own damage."),
                color=CardType.Black,
                holder=None,
                is_equip=False,
                use=single_use.vampire_bat
            ),
            card.Card(
                title="Vampire Bat",
                desc=("You give 2 points of damage to any character"
                      " and heal 1 point of your own damage."),
                color=CardType.Black,
                holder=None,
                is_equip=False,
                use=single_use.vampire_bat
            ),
            card.Card(
                title="Vampire Bat",
                desc=("You give 2 points of damage to any character"
                      " and heal 1 point of your own damage."),
                color=CardType.Black,
                holder=None,
                is_equip=False,
                use=single_use.vampire_bat
            ),
            card.Card(
                title="Diabolic Ritual",
                desc=("If you are a Shadow, you may reveal your identity."
                      " If you do, you fully heal you damage."),
                color=CardType.Black,
                holder=None,
                is_equip=False,
                use=single_use.diabolic_ritual
            ),
            card.Card(
                title="Banana Peel",
                desc=("Give one of your equipment cards to another character. "
                      "If you have no equipment cards,"
                      " you receive 1 point of damage."),
                color=CardType.Black,
                holder=None,
                is_equip=False,
                use=single_use.banana_peel
            ),
            card.Card(
                title="Dynamite",
                desc=("Roll 2 dice and give 3 points of damage to all"
                      " characters in the area designated "
                      "by the total number rolled "
                      "(nothing happens if a 7 is rolled)."),
                color=CardType.Black,
                holder=None,
                is_equip=False,
                use=single_use.dynamite
            ),
            card.Card(
                title="Spiritual Doll",
                desc=("Pick a character and roll the 6-sided die. "
                      "If the die number is 1 to 4, "
                      "you give 3 points of damage to that character. "
                      "If the die number is 5 or 6, "
                      "you get 3 points of damage."),
                color=CardType.Black,
                holder=None,
                is_equip=False,
                use=single_use.spiritual_doll
            )
        ]

        # Initialize hermit cards
        hermit_cards = [
            card.Card(
                title="Hermit\'s Blackmail",
                desc=("I bet you're either a Neutral or a Hunter. "
                      "If so, you must either give an Equipment card"
                      " to the current player or receive 1 damage!"),
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.blackmail
            ),
            card.Card(
                title="Hermit\'s Blackmail",
                desc=("I bet you're either a Neutral or a Hunter. "
                      "If so, you must either give an Equipment card"
                      " to the current player or receive 1 damage!"),
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.blackmail
            ),
            card.Card(
                title="Hermit\'s Greed",
                desc=("I bet you're either a Neutral or a Shadow. "
                      "If so, you must either give an Equipment card"
                      " to the current player or receive 1 damage!"),
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.greed
            ),
            card.Card(
                title="Hermit\'s Greed",
                desc=("I bet you're either a Neutral or a Shadow. "
                      "If so, you must either give an Equipment card"
                      " to the current player or receive 1 damage!"),
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.greed
            ),
            card.Card(
                title="Hermit\'s Anger",
                desc=("I bet you're either a Hunter or a Shadow. "
                      "If so, you must either give an Equipment card"
                      " to the current player or receive 1 damage!"),
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.anger
            ),
            card.Card(
                title="Hermit\'s Anger",
                desc=("I bet you're either a Hunter or a Shadow. "
                      "If so, you must either give an Equipment card"
                      " to the current player or receive 1 damage!"),
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.anger
            ),
            card.Card(
                title="Hermit\'s Slap",
                desc="I bet you're a Hunter. If so, you receive 1 damage!",
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.slap
            ),
            card.Card(
                title="Hermit\'s Slap",
                desc="I bet you're a Hunter. If so, you receive 1 damage!",
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.slap
            ),
            card.Card(
                title="Hermit\'s Spell",
                desc="I bet you're a Shadow. If so, you receive 1 damage!",
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.spell
            ),
            card.Card(
                title="Hermit\'s Exorcism",
                desc="I bet you're a Shadow. If so, you receive 2 damage!",
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.exorcism
            ),
            card.Card(
                title="Hermit\'s Nurturance",
                desc=("I bet you're a Neutral. If so, you heal 1 damage! "
                      "(However, if you have no damage, "
                      "then you receive 1 damage!)"),
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.nurturance
            ),
            card.Card(
                title="Hermit\'s Aid",
                desc=("I bet you're a Hunter. If so, you heal 1 damage! "
                      "(However, if you have no damage, "
                      "then you receive 1 damage!)"),
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.aid
            ),
            card.Card(
                title="Hermit\'s Huddle",
                desc=("I bet you're a Shadow. If so, you heal 1 damage! "
                      "(However, if you have no damage, "
                      "then you receive 1 damage!)"),
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.huddle
            ),
            card.Card(
                title="Hermit\'s Lesson",
                desc=("I bet your maximum HP is 12 or more. "
                      "If so, you receive 2 damage!"),
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.lesson
            ),
            card.Card(
                title="Hermit\'s Bully",
                desc=("I bet your maximum HP is 11 or less. "
                      "If so, you receive 1 damage!"),
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.bully
            ),
            card.Card(
                title="Hermit\'s Prediction",
                desc=("You must reveal your character information "
                      "secretly to the current player!"),
                color=CardType.Hermit,
                holder=None,
                is_equip=False,
                use=hermit.prediction
            )
        ]

        # Initialize white, black, hermit decks
        self.WHITE_DECK = deck.Deck(cards=white_cards)
        self.BLACK_DECK = deck.Deck(cards=black_cards)
        self.HERMIT_DECK = deck.Deck(cards=hermit_cards)

        # Initialize characters

        self.CHARACTERS = [
            character.Character(
                name="Valkyrie",
                alleg=Alleg.Shadow,
                max_damage=13,
                win_cond=win_conditions.shadow,
                win_cond_desc="All of the Hunters (or 3 Neutrals) are dead.",
                special=specials.valkyrie,
                special_desc=("When you attack, you only roll the 4-sided die"
                              " and inflict the amount of damage rolled."),
                resource_id="valkyrie"
            ),
            character.Character(
                name="Vampire",
                alleg=Alleg.Shadow,
                max_damage=13,
                win_cond=win_conditions.shadow,
                win_cond_desc="All of the Hunters (or 3 Neutrals) are dead.",
                special=specials.vampire,
                special_desc=("If you attack a player and inflict damage, "
                              "you heal 2 points of your own damage."),
                resource_id="vampire"
            ),
            character.Character(
                name="Werewolf",
                alleg=Alleg.Shadow,
                max_damage=14,
                win_cond=win_conditions.shadow,
                win_cond_desc="All of the Hunters (or 3 Neutrals) are dead.",
                special=specials.werewolf,
                special_desc=("After you are attacked, "
                              "you can counterattack immediately."),
                resource_id="werewolf"
            ),
            character.Character(
                name="Ultra Soul",
                alleg=Alleg.Shadow,
                max_damage=11,
                win_cond=win_conditions.shadow,
                win_cond_desc="All of the Hunters (or 3 Neutrals) are dead.",
                special=specials.ultra_soul,
                special_desc=("When your turn starts, you can give 3 damage"
                              " to one player who is at"
                              " the Underworld Gate."),
                resource_id="ultra-soul"
            ),
            # character.Character(
            #     name="Wight",
            #     alleg=Alleg.Shadow,
            #     max_damage=14,
            #     win_cond=win_conditions.shadow,
            #     win_cond_desc="All of the Hunters (or 3 Neutrals) are dead.",
            #     special=specials.wight,
            #     special_desc=("Once per game, when your turn is over, you may"
            #                   " take an additional number of turns equal to the"
            #                   " amount of dead characters."),
            #     resource_id="wight"
            # ),
            character.Character(
                name="Allie",
                alleg=Alleg.Neutral,
                max_damage=8,
                win_cond=win_conditions.allie,
                win_cond_desc="You're not dead when the game is over.",
                special=specials.allie,
                special_desc="Once per game, you may fully heal your damage.",
                resource_id="allie"
            ),
            character.Character(
                name="Bob",
                alleg=Alleg.Neutral,
                max_damage=10,
                win_cond=win_conditions.bob,
                win_cond_desc="You have 5 or more equipment cards.",
                special=specials.bob,
                special_desc=("If your attack inflicts 2 or more damage, "
                              "you may steal an Equipment card from your"
                              " target instead of giving damage."),
                resource_id="bob1",
                modifiers={'min_players': 4, 'max_players': 6}
            ),
            character.Character(
                name="Bob",
                alleg=Alleg.Neutral,
                max_damage=10,
                win_cond=win_conditions.bob,
                win_cond_desc="You have 5 or more equipment cards.",
                special=specials.bob,
                special_desc=("If you kill another player, "
                              "you may take all of their Equipment cards."),
                resource_id="bob2",
                modifiers={'min_players': 7, 'max_players': 8}
            ),
            character.Character(
                name="Catherine",
                alleg=Alleg.Neutral,
                max_damage=11,
                win_cond=win_conditions.catherine,
                win_cond_desc=("You are either the first to die or one of the"
                               " last two players alive."),
                special=specials.catherine,
                special_desc="When your turn starts, you heal 1 damage.",
                resource_id="catherine"
            ),
            # character.Character(
            #     name="Charles",
            #     alleg=Alleg.Neutral,
            #     max_damage=11,
            #     win_cond=win_conditions.charles,
            #     win_cond_desc=("You kill another character after at least two"
            #                    " characters are already dead."),
            #     special=specials.charles,
            #     special_desc=("After you attack, you may give yourself 2 points"
            #                   " of damage to attack the same character again."),
            #     resource_id="charles"
            # ),
            character.Character(
                name="Gregor",
                alleg=Alleg.Hunter,
                max_damage=14,
                win_cond=win_conditions.hunter,
                win_cond_desc="All of the Shadows are dead.",
                special=specials.gregor,
                special_desc=("Once per game, when your turn is over, you may"
                              " protect yourself from receiving any damage"
                              " until the start of your next turn."),
                resource_id="gregor"
            ),
            character.Character(
                name="George",
                alleg=Alleg.Hunter,
                max_damage=14,
                win_cond=win_conditions.hunter,
                win_cond_desc="All of the Shadows are dead.",
                special=specials.george,
                special_desc=("Once per game, when your turn starts, you can"
                              " pick a player and damage them for the"
                              " roll of a 4-sided die."),
                resource_id="george"
            ),
            character.Character(
                name="Fu-ka",
                alleg=Alleg.Hunter,
                max_damage=12,
                win_cond=win_conditions.hunter,
                win_cond_desc="All of the Shadows are dead.",
                special=specials.fuka,
                special_desc=("Once per game, when your turn starts, "
                              "you can set the damage of any player to 7."),
                resource_id="fu-ka"
            ),
            character.Character(
                name="Franklin",
                alleg=Alleg.Hunter,
                max_damage=12,
                win_cond=win_conditions.hunter,
                win_cond_desc="All of the Shadows are dead.",
                special=specials.franklin,
                special_desc=("Once per game, when your turn starts, "
                              "you can pick a player and damage"
                              " them for the roll of a 6-sided die."),
                resource_id="franklin"
            ),
            character.Character(
                name="Ellen",
                alleg=Alleg.Hunter,
                max_damage=10,
                win_cond=win_conditions.hunter,
                win_cond_desc="All of the Shadows are dead.",
                special=specials.ellen,
                special_desc=("Once per game, when your turn starts, "
                              "you can choose a player and permanently"
                              " void their special ability."),
                resource_id="ellen"
            )
        ]

        # Initialize areas
        self.AREAS = [
            area.Area(
                name="Hermit's Cabin",
                desc="Draw a Hermit Card.",
                domain=[2, 3],
                action=lambda gc, player: player.drawCard(gc.hermit_cards),
                resource_id="hermits-cabin"
            ),
            area.Area(
                name="Underworld Gate",
                desc="Draw a card from the deck of your choice.",
                domain=[4, 5],
                action=area.underworld_gate_action,
                resource_id="underworld-gate"
            ),
            area.Area(
                name="Church",
                desc="Draw a White Card.",
                domain=[6],
                action=lambda gc, player: player.drawCard(gc.white_cards),
                resource_id="church"
            ),
            area.Area(
                name="Cemetery",
                desc="Draw a Black Card.",
                domain=[8],
                action=lambda gc, player: player.drawCard(gc.black_cards),
                resource_id="cemetery"
            ),
            area.Area(
                name="Weird Woods",
                desc="Heal 1 damage or give 2 damage to any player.",
                domain=[9],
                action=area.weird_woods_action,
                resource_id="weird-woods"
            ),
            area.Area(
                name="Erstwhile Altar",
                desc="Steal an equipment card from any player.",
                domain=[10],
                action=area.erstwhile_altar_action,
                resource_id="erstwhile-altar"
            )
        ]
