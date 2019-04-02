import card, deck, character, area

# elements.py
# Encodes all characters, win conditions, special abilities,
# game areas, decks, and cards in an element factory. Every
# game context is initialized with its own element factory.

## Enum for allegiances
ALLEGIANCE_MAP = {
    0: "Shadow",
    1: "Neutral",
    2: "Hunter"
}

## Enum for card types
CARD_COLOR_MAP = {
    0: "White",
    1: "Black",
    2: "Green"
}

class ElementFactory:
    def __init__(self):

        ## Helper functions for asking players to make choices

        def choose_player(args):

            # Select a player from all live playerts who arent you
            args['self'].gc.tell_h("{} is choosing a player...".format(args['self'].user_id))
            data = {'options': [p.user_id for p in args['self'].gc.getLivePlayers() if p != args['self']]}
            target = args['self'].ask_h('select', data, args['self'].user_id)['value']

            # Return the chosen player
            target_Player = [p for p in args['self'].gc.getLivePlayers() if p.user_id == target][0]
            args['self'].gc.tell_h("{} chose {}!".format(args['self'].user_id, target))
            return target_Player

        def choose_equipment(player, target):

            # Select an equipment card belonging to the given target
            data = {'options': [eq.title for eq in target.equipment]}
            equip = target.ask_h('select', data, player.user_id)['value']

            # Return the selected equipment card
            equip_Equipment = [eq for eq in target.equipment if eq.title == equip][0]
            return equip_Equipment

        ## White card usage functions

        def use_first_aid(args):

            # Select a player to use card on (includes user)
            args['self'].ask_h('confirm', {'options': ["Use First Aid"]}, args['self'].user_id)
            data = {'options': [t.user_id for t in args['self'].gc.getLivePlayers()]}
            target = args['self'].ask_h('select', data, args['self'].user_id)['value']

            # Set selected player to 7 damage
            [p for p in args['self'].gc.getLivePlayers() if p.user_id == target][0].setDamage(7)

        def use_judgement(args):

            # Give all players except user 2 damage
            args['self'].ask_h('confirm', {'options': ["Unleash judgement"]}, args['self'].user_id)
            for p in args['self'].gc.getLivePlayers():
                if p != args['self']:
                    p.moveDamage(-2, args['self'])

        def use_holy_water(args):

            # Heal user by 2 damage
            args['self'].ask_h('confirm', {'options': ["Heal yourself"]}, args['self'].user_id)
            args['self'].moveDamage(2, args['self'])

        def use_advent(args):

            # If hunter, can reveal and heal fully, or heal fully if already revealed
            data = {'options': ["Do nothing"]}
            if args['self'].character.alleg == 2:
                if args['self'].state == 2:
                    data['options'].append("Reveal and heal fully")
                else:
                    data['options'].append("Heal fully")

            # Get decision and take corresponding action
            decision = args['self'].ask_h('yesno', data, args['self'].user_id)['value']
            if decision == "Do nothing":
                args['self'].gc.tell_h("{} did nothing.".format(args['self'].user_id))
            elif decision == "Reveal and heal fully":
                args['self'].reveal()
                args['self'].setDamage(0, args['self'])
            else:
                args['self'].setDamage(0, args['self'])

        def use_disenchant_mirror(args):

            # If shadow and not unknown, force reveal
            data = {'options': ["Do nothing"]}
            if args['self'].character.alleg == 0 and args['self'].character.name != "Unknown":
                data = {'options': ["Reveal yourself"]}

            # Reveal character, or do nothing if hunter
            decision = args['self'].ask_h('yesno', data, args['self'].user_id)['value']
            if decision == "Do nothing":
                args['self'].gc.tell_h("{} did nothing.".format(args['self'].user_id))
            else:
                args['self'].reveal()

        def use_blessing(args):

            # Choose a player to use blessing on
            args['self'].ask_h('confirm', {'options': ["Bless someone"]}, args['self'].user_id)
            target = choose_player(args)

            # Roll dice to get value to heal by
            args['self'].gc.tell_h("{} is rolling the 6-sided die...".format(args['self'].user_id))
            data = {'options': ['Roll the 6-sided die']}
            args['self'].ask_h('confirm', data, args['self'].user_id)
            roll_result = args['self'].gc.die6.roll()
            args['self'].gc.tell_h("{} rolled a {}!".format(args['self'].user_id, roll_result))

            # Heal target player
            target.moveDamage(roll_result, args['self'])

        def use_chocolate(args):

            # If low-hp character, can reveal and heal fully, or heal fully if already revealed
            data = {'options': ["Do nothing"]}
            if args['self'].character.name in ["Allie", "Agnes", "Emi", "Ellen", "Ultra Soul", "Unknown"]:
                if args['self'].state == 2:
                    data['options'].append("Reveal and heal fully")
                else:
                    data['options'].append("Heal fully")

            # Get decision and take corresponding action
            decision = args['self'].ask_h('yesno', data, args['self'].user_id)['value']
            if decision == "Do nothing":
                args['self'].gc.tell_h("{} did nothing.".format(args['self'].user_id))
            elif decision == "Reveal and heal fully":
                args['self'].reveal()
                args['self'].setDamage(0, args['self'])
            else:
                args['self'].setDamage(0, args['self'])

        def use_concealed_knowledge(args):

            # Change turn order so that current player goes again
            args['self'].ask_h('confirm', {'options': ["Reveal Concealed Knowledge"]}, args['self'].user_id)
            args['self'].gc.turn_order.insert(args['self'].gc.turn_order.index(args['self']), args['self'])

        def use_guardian_angel(args):

            # user can't take damage until their next turn (this is checked in player.defend()
            # and player.takeTurn()
            args['self'].ask_h('confirm', {'options': ["Summon a Guardian Angel"]}, args['self'].user_id)
            args['self'].modifiers['guardian_angel'] = True

        ## Initialize white cards

        WHITE_CARDS = [
            card.Card(
                title = "Advent",
                desc = ("If you are a Hunter, you may reveal your identity. "
                        "If you do, or if you are already revealed, you heal fully."),
                color = 0,
                holder = None,
                is_equip = False,
                use = use_advent
            ),
            card.Card(
                title = "Disenchant Mirror",
                desc = "If you are a Shadow, except for Unknown, you must reveal your identity.",
                color = 0,
                holder = None,
                is_equip = False,
                use = use_disenchant_mirror
            ),
            card.Card(
                title = "Blessing",
                desc = ("Pick a character other than yourself and roll the 6-sided die. "
                        "That character heals an amount of damage equal to the die roll."),
                color = 0,
                holder = None,
                is_equip = False,
                use = use_blessing
            ),
            card.Card(
                title = "Chocolate",
                desc = ("If you are Allie, Agnes, Emi, Ellen, Unknown, or Ultra Soul, you may reveal your identity. "
                        "If you do, or if you are already revealed, you heal fully."),
                color = 0,
                holder = None,
                is_equip = False,
                use = use_chocolate
            ),
            card.Card(
                title = "Concealed Knowledge",
                desc = "When this turn is over, it will be your turn again.",
                color = 0,
                holder = None,
                is_equip = False,
                use = use_concealed_knowledge
            ),
            card.Card(
                title = "Guardian Angel",
                desc = "You take no damage from the direct attacks of other characters until the start of your next turn.",
                color = 0,
                holder = None,
                is_equip = False,
                use = use_guardian_angel
            ),
            card.Card(
                title = "Holy Robe",
                desc = "Your attacks do 1 less damage and the amount of damage you receive from attacks is reduced by 1 point.",
                color = 0, # 0 : WHITE
                holder = None,
                is_equip = True,
                use = lambda is_attack, successful, amt: max(0, amt - 1) # applies to both attack and defend
            ),
            card.Card(
                title = "Flare of Judgement",
                desc = "All characters except yourself receive 2 points of damage.",
                color = 0,
                holder = None,
                is_equip = False,
                use = use_judgement
            ),
            card.Card(
                title = "First Aid",
                desc = "Place a character's damage marker to 7 (You can choose yourself).",
                color = 0,
                holder = None,
                is_equip = False,
                use = use_first_aid
            ),
            card.Card(
                title = "Holy Water of Healing",
                desc = "Heal 2 points of your damage.",
                color = 0,
                holder = None,
                is_equip = False,
                use = use_holy_water
            ),
            card.Card(
                title = "Holy Water of Healing",
                desc = "Heal 2 points of your damage.",
                color = 0,
                holder = None,
                is_equip = False,
                use = use_holy_water
            )
        ]

        ## Black card usage functions

        def use_bloodthirsty_spider(args):

            # Choose a player to attack
            args['self'].ask_h('confirm', {'options': ["Summon a Bloodthirsty Spider"]}, args['self'].user_id)
            target = choose_player(args)

            # Both the target and the user take 2 damage
            target.moveDamage(-2, args['self'])
            args['self'].moveDamage(-2, args['self'])

        def use_vampire_bat(args):

            # Choose a player to attack
            args['self'].ask_h('confirm', {'options': ["Summon a Vampire Bat"]}, args['self'].user_id)
            target = choose_player(args)

            # Target takes 2 damage, user heals 1 damage
            target.moveDamage(-2, args['self'])
            args['self'].moveDamage(1, args['self'])

        def use_moody_goblin(args):

            # Get players who have equipment
            args['self'].ask_h('confirm', {'options': ["Steal an Equipment Card"]}, args['self'].user_id)
            players_w_items = [p for p in args['self'].gc.getLivePlayers() if (len(p.equipment) and p != args['self'])]

            # If someone has equipment and isn't user, offer choice
            if len(players_w_items):

                # Choose who to steal from
                data = {'options': [p.user_id for p in players_w_items]}
                target = args['self'].ask_h('select', data, args['self'].user_id)['value']

                # Get target player and their equipment
                target_Player = [p for p in args['self'].gc.getLivePlayers() if p.user_id == target][0]
                data = {'options': [eq.title for eq in target_Player.equipment]}

                # Choose which equipment to take
                equip = args['self'].ask_h('select', data, args['self'].user_id)['value']
                equip_Equipment = [eq for eq in target_Player.equipment if eq.title == equip][0]

                # Transfer equipment from one player to the other
                i = target_Player.equipment.index(equip_Equipment)
                equip_Equipment = target_Player.equipment.pop(i)
                args['self'].equipment.append(equip_Equipment)
                equip_Equipment.holder = args['self']
                args['self'].gc.tell_h("{} stole {}'s {}!".format(args['self'].user_id, target_Player.user_id, equip_Equipment.title))

                # Update frontend with transfer
                args['self'].gc.update_h()

            else:

                # No one has equipment to steal, do nothing
                args['self'].gc.tell_h("Nobody has any items for {} to steal.".format(args['self'].user_id))

        def use_diabolic_ritual(args):

            # If shadow, can reveal and heal fully
            data = {'options': ["Do nothing"]}
            if args['self'].character.alleg == 0 and args['self'].state != 1:
                data['options'].append("Reveal and heal fully")

            # Get decision and take corresponding action
            decision = args['self'].ask_h('yesno', data, args['self'].user_id)['value']
            if decision == "Do nothing":
                args['self'].gc.tell_h("{} did nothing.".format(args['self'].user_id))
            else:
                args['self'].reveal()
                args['self'].setDamage(0, args['self'])

        def use_banana_peel(args):

            # If have equipment, must give away one or take damage. If no equipment, must take damage
            if len(args['self'].equipment):
                data = {'options': ["Give an equipment card", "Receive 1 damage"]}
            else:
                data = {'options': ["Receive 1 damage"]}

            # Get decision and take action
            decision = args['self'].ask_h('yesno', data, args['self'].user_id)['value']
            if decision == "Give an equipment card":

                # Choose an equipment card to give away
                args['self'].gc.tell_h("{} is choosing an equipment card to give away...".format(args['self'].user_id))
                eq = choose_equipment(args['self'], args['self'])

                # Choose someone to give to
                receiver = choose_player(args)

                # Transfer equipment from one player to the other
                i = args['self'].equipment.index(eq)
                eq = args['self'].equipment.pop(i)
                receiver.equipment.append(eq)
                eq.holder = receiver
                args['self'].gc.tell_h("{} gave {} their {}!".format(args['self'].user_id, receiver.user_id, eq.title))

                # Update frontend
                args['self'].gc.update_h()

            else:

                # Take 1 damage
                args['self'].moveDamage(-1, args['self'])

        def use_dynamite(args):

            # Roll to find out which area gets hit
            args['self'].ask_h('confirm', {'options': ["Light the fuse"]}, args['self'].user_id)
            args['self'].gc.tell_h("{} is rolling for where the dynamite lands...".format(args['self'].user_id))
            data = {'options': ['Roll for area']}
            args['self'].ask_h('confirm', data, args['self'].user_id)
            roll_result_4 = args['self'].gc.die4.roll()
            roll_result_6 = args['self'].gc.die6.roll()
            roll_result = roll_result_4 + roll_result_6
            args['self'].gc.tell_h("{} rolled {} + {} = {}!".format(args['self'].user_id, roll_result_4, roll_result_6, roll_result))

            # Hit area corresponding to roll number
            if roll_result == 7:

                # No area has 7 on it
                args['self'].gc.tell_h("Nothing happens.")

            else:

                # Get area from roll result
                destination_Area = None
                for z in args['self'].gc.zones:
                    for a in z.areas:
                        if roll_result in a.domain:
                            destination_Area = a
                destination = destination_Area.name

                # Hit all players in area for 3 damage
                args['self'].gc.tell_h("Dynamite blew up the {}!".format(destination))
                affected_players = [p for p in args['self'].gc.players if p.location == destination_Area]
                for p in affected_players:
                    p.moveDamage(-3, args['self'])

        def use_spiritual_doll(args):

            # Choose a player to target
            args['self'].ask_h('confirm', {'options': ["Use Spiritual Doll"]}, args['self'].user_id)
            target = choose_player(args)

            # Roll 6-sided die
            args['self'].gc.tell_h("{} is rolling the 6-sided die...".format(args['self'].user_id))
            data = {'options': ['Roll the 6-sided die']}
            args['self'].ask_h('confirm', data, args['self'].user_id)
            roll_result = args['self'].gc.die6.roll()
            args['self'].gc.tell_h("{} rolled a {}!".format(args['self'].user_id, roll_result))

            # If roll is >= 5, user takes 3 damage. Otherwise, target takes 3 damage.
            if roll_result >= 5:
                args['self'].moveDamage(-3, args['self'])
            else:
                target.moveDamage(-3, args['self'])

        ## Initialize black cards

        BLACK_CARDS = [
            card.Card(
                title = "Butcher Knife",
                desc = "If your attack is successful, you give 1 point of extra damage.",
                color = 1, # 1 : BLACK
                holder = None,
                is_equip = True,
                use = lambda is_attack, successful, amt: amt + 1 if (is_attack and successful) else amt
            ),
            card.Card(
                title = "Chainsaw",
                desc = "If your attack is successful, you give 1 point of extra damage.",
                color = 1,
                holder = None,
                is_equip = True,
                use = lambda is_attack, successful, amt: amt + 1 if (is_attack and successful) else amt
            ),
            card.Card(
                title = "Rusted Broad Axe",
                desc = "If your attack is successful, you give 1 point of extra damage.",
                color = 1,
                holder = None,
                is_equip = True,
                use = lambda is_attack, successful, amt: amt + 1 if (is_attack and successful) else amt
            ),
            card.Card(
                title = "Moody Goblin",
                desc = "You steal an equipment card from any character.",
                color = 1,
                holder = None,
                is_equip = False,
                use = use_moody_goblin
            ),
            card.Card(
                title = "Moody Goblin",
                desc = "You steal an equipment card from any character.",
                color = 1,
                holder = None,
                is_equip = False,
                use = use_moody_goblin
            ),
            card.Card(
                title = "Bloodthirsty Spider",
                desc = "You give 2 points of damage to any character and receive 2 points of damage yourself.",
                color = 1,
                holder = None,
                is_equip = False,
                use = use_bloodthirsty_spider
            ),
            card.Card(
                title = "Vampire Bat",
                desc = "You give 2 points of damage to any character and heal 1 point of your own damage.",
                color = 1,
                holder = None,
                is_equip = False,
                use = use_vampire_bat
            ),
            card.Card(
                title = "Vampire Bat",
                desc = "You give 2 points of damage to any character and heal 1 point of your own damage.",
                color = 1,
                holder = None,
                is_equip = False,
                use = use_vampire_bat
            ),
            card.Card(
                title = "Vampire Bat",
                desc = "You give 2 points of damage to any character and heal 1 point of your own damage.",
                color = 1,
                holder = None,
                is_equip = False,
                use = use_vampire_bat
            ),
            card.Card(
                title = "Diabolic Ritual",
                desc = "If you are a Shadow, you may reveal your identity. If you do, you fully heal you damage.",
                color = 1,
                holder = None,
                is_equip = False,
                use = use_diabolic_ritual
            ),
            card.Card(
                title = "Banana Peel",
                desc = ("Give one of your equipment cards to another character. "
                        "If you have no equipment cards, you receive 1 point of damage."),
                color = 1,
                holder = None,
                is_equip = False,
                use = use_banana_peel
            ),
            card.Card(
                title = "Dynamite",
                desc = ("Roll 2 dice and give 3 points of damage to all characters in the area designated "
                        "by the total number rolled (nothing happens if a 7 is rolled)."),
                color = 1,
                holder = None,
                is_equip = False,
                use = use_dynamite
            ),
            card.Card(
                title = "Spiritual Doll",
                desc = ("Pick a character and roll the 6-sided die. "
                        "If the die number is 1 to 4, you give 3 points of damage to that character. "
                        "If the die number is 5 or 6, you get 3 points of damage."),
                color = 1,
                holder = None,
                is_equip = False,
                use = use_spiritual_doll
            )
        ]

        ## Hermit card usage functions

        def hermit_blackmail(args):

            # Choose a player to give the card to
            args['self'].ask_h('confirm', {'options': ["Use Hermit's Blackmail"]}, args['self'].user_id)
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            # If target is neutral or hunter, must give equipment or take 1 damage
            if target.character.alleg > 0:

                # Target is neutral or hunter, get decision
                target.gc.direct_h("You are a {}. Make a choice.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                if len(target.equipment):
                    data = {'options': ["Give an equipment card", "Receive 1 damage"]}
                else:
                    data = {'options': ["Receive 1 damage"]}
                decision = target.ask_h('yesno', data, target.user_id)['value']

                # Branch on decision
                if decision == "Give an equipment card":

                    # Target chooses an equipment card to give away
                    target.gc.tell_h("{} is choosing an equipment card to give to {}...".format(target.user_id, args['self'].user_id))
                    eq = choose_equipment(target, target)

                    # Transfer equipment from target to user
                    i = target.equipment.index(eq)
                    eq = target.equipment.pop(i)
                    args['self'].equipment.append(eq)
                    eq.holder = args['self']
                    args['self'].gc.tell_h("{} gave {} their {}!".format(target.user_id, args['self'].user_id, eq.title))

                    # Update frontend with transfer
                    target.gc.update_h()

                else:

                    # Target takes 1 damage
                    new_damage = target.moveDamage(-1, args['self'])
                    target.gc.tell_h("{} took 1 damage!".format(target.user_id))

            else:

                # Target is a shadow, nothing happens
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('confirm', data, target.user_id)
                target.gc.tell_h("{} did nothing.".format(target.user_id))

        def hermit_greed(args):

            # Choose a player to give the card to
            args['self'].ask_h('confirm', {'options': ["Use Hermit's Greed"]}, args['self'].user_id)
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            # If target is neutral or shadow, must give equipment or take 1 damage
            if target.character.alleg < 2:

                # Target is neutral or shadow, get decision
                target.gc.direct_h("You are a {}. Make a choice.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                if len(target.equipment):
                    data = {'options': ["Give an equipment card", "Receive 1 damage"]}
                else:
                    data = {'options': ["Receive 1 damage"]}
                decision = target.ask_h('yesno', data, target.user_id)['value']

                # Branch on decision
                if decision == "Give an equipment card":

                    # Target chooses an equipment card to give away
                    target.gc.tell_h("{} is choosing an equipment card to give to {}...".format(target.user_id, args['self'].user_id))
                    eq = choose_equipment(target, target)

                    # Transfer equipment from target to user
                    i = target.equipment.index(eq)
                    eq = target.equipment.pop(i)
                    args['self'].equipment.append(eq)
                    eq.holder = args['self']
                    args['self'].gc.tell_h("{} gave {} their {}!".format(target.user_id, args['self'].user_id, eq.title))

                    # Update frontend with transfer
                    target.gc.update_h()

                else:

                    # Target takes 1 damage
                    new_damage = target.moveDamage(-1, args['self'])
                    target.gc.tell_h("{} took 1 damage!".format(target.user_id))

            else:

                # Target is a hunter, nothing happens
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('confirm', data, target.user_id)
                target.gc.tell_h("{} did nothing.".format(target.user_id))

        def hermit_anger(args):

            # Choose a player to give the card to
            args['self'].ask_h('confirm', {'options': ["Use Hermit's Anger"]}, args['self'].user_id)
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            # If target is hunter or shadow, must give equipment or take 1 damage
            if target.character.alleg in [0, 2]:

                # Target is hunter or shadow, get decision
                target.gc.direct_h("You are a {}. Make a choice.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                if len(target.equipment):
                    data = {'options': ["Give an equipment card", "Receive 1 damage"]}
                else:
                    data = {'options': ["Receive 1 damage"]}
                decision = target.ask_h('yesno', data, target.user_id)['value']

                # Branch on decision
                if decision == "Give an equipment card":

                    # Target chooses an equipment card to give away
                    target.gc.tell_h("{} is choosing an equipment card to give to {}...".format(target.user_id, args['self'].user_id))
                    eq = choose_equipment(target, target)

                    # Transfer equipment from target to user
                    i = target.equipment.index(eq)
                    eq = target.equipment.pop(i)
                    args['self'].equipment.append(eq)
                    eq.holder = args['self']
                    args['self'].gc.tell_h("{} gave {} their {}!".format(target.user_id, args['self'].user_id, eq.title))

                    # Update frontend with transfer
                    target.gc.update_h()
                else:

                    # Target takes 1 damage
                    new_damage = target.moveDamage(-1, args['self'])
                    target.gc.tell_h("{} took 1 damage!".format(target.user_id))

            else:

                # Target is a neutral, nothing happens
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('confirm', data, target.user_id)
                target.gc.tell_h("{} did nothing.".format(target.user_id))

        def hermit_slap(args):

            # Choose a player to give the card to
            args['self'].ask_h('confirm', {'options': ["Use Hermit's Slap"]}, args['self'].user_id)
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            # If hunter, take 1 damage
            if target.character.alleg == 2:

                # Prompt target to receive 1 damage
                target.gc.direct_h("You are a {}.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ["Receive 1 damage"]}
                target.ask_h('confirm', data, target.user_id)

                # Give 1 damage to target
                new_damage = target.moveDamage(-1, args['self'])
                target.gc.tell_h("{} took 1 damage!".format(target.user_id))
            else:

                # Target is not a hunter, nothing happens
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('confirm', data, target.user_id)
                target.gc.tell_h("{} did nothing.".format(target.user_id))

        def hermit_spell(args):

            # Choose a player to give the card to
            args['self'].ask_h('confirm', {'options': ["Use Hermit's Spell"]}, args['self'].user_id)
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            # If shadow, take 1 damage
            if target.character.alleg == 0:

                # Prompt target to receive 1 damage
                target.gc.direct_h("You are a {}.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ["Receive 1 damage"]}
                target.ask_h('confirm', data, target.user_id)

                # Give 1 damage to target
                new_damage = target.moveDamage(-1, args['self'])
                target.gc.tell_h("{} took 1 damage!".format(target.user_id))

            else:

                # Target is not a shadow, nothing happens
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('confirm', data, target.user_id)
                target.gc.tell_h("{} did nothing.".format(target.user_id))

        def hermit_exorcism(args):

            # Choose a player to give the card to
            args['self'].ask_h('confirm', {'options': ["Use Hermit's Exorcism"]}, args['self'].user_id)
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            # If shadow, take 2 damage
            if target.character.alleg == 0:

                # Prompt target to receive 2 damage
                target.gc.direct_h("You are a {}.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ["Receive 2 damage"]}
                target.ask_h('confirm', data, target.user_id)

                # Give 2 damage to target
                new_damage = target.moveDamage(-2, args['self'])
                target.gc.tell_h("{} took 2 damage!".format(target.user_id))

            else:

                # Target is not a shadow, nothing happens
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('confirm', data, target.user_id)
                target.gc.tell_h("{} did nothing.".format(target.user_id))

        def hermit_nurturance(args):

            # Choose a player to give the card to
            args['self'].ask_h('confirm', {'options': ["Use Hermit's Nurturance"]}, args['self'].user_id)
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            # If neutral, heal 1 damage (unless at 0, then take 1 damage)
            if target.character.alleg == 1:

                # Branch on hp value
                target.gc.direct_h("You are a {}.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                if target.damage == 0:

                    # Hp is 0, prompt to receive 1 damage
                    data = {'options': ["Receive 1 damage"]}
                    target.ask_h('confirm', data, target.user_id)

                    # Give target 1 damage
                    new_damage = target.moveDamage(-1, args['self'])
                    target.gc.tell_h("{} took 1 damage!".format(target.user_id))

                else:

                    # Hp is nonzero, prompt to heal 1 damage
                    data = {'options': ["Heal 1 damage"]}
                    target.ask_h('confirm', data, target.user_id)

                    # Heal target 1 damage
                    new_damage = target.moveDamage(1, args['self'])
                    target.gc.tell_h("{} healed 1 damage!".format(target.user_id))

            else:

                # Target is not a neutral, nothing happens
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('confirm', data, target.user_id)
                target.gc.tell_h("{} did nothing.".format(target.user_id))

        def hermit_aid(args):

            # Choose a player to give the card to
            args['self'].ask_h('confirm', {'options': ["Use Hermit's Aid"]}, args['self'].user_id)
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            # If hunter, heal 1 damage (unless at 0, then take 1 damage)
            if target.character.alleg == 2:

                # Branch on hp value
                target.gc.direct_h("You are a {}.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                if target.damage == 0:

                    # Hp is 0, prompt to receive 1 damage
                    data = {'options': ["Receive 1 damage"]}
                    target.ask_h('confirm', data, target.user_id)

                    # Give target 1 damage
                    new_damage = target.moveDamage(-1, args['self'])
                    target.gc.tell_h("{} took 1 damage!".format(target.user_id))

                else:

                    # Hp is nonzero, prompt to heal 1 damage
                    data = {'options': ["Heal 1 damage"]}
                    target.ask_h('confirm', data, target.user_id)

                    # Heal target 1 damage
                    new_damage = target.moveDamage(1, args['self'])
                    target.gc.tell_h("{} healed 1 damage!".format(target.user_id))

            else:

                # Target is not a hunter, nothing happens
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('confirm', data, target.user_id)
                target.gc.tell_h("{} did nothing.".format(target.user_id))

        def hermit_huddle(args):

            # Choose a player to give the card to
            args['self'].ask_h('confirm', {'options': ["Use Hermit's Huddle"]}, args['self'].user_id)
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            # If shadow, heal 1 damage (unless at 0, then take 1 damage)
            if target.character.alleg == 0:

                # Branch on hp value
                target.gc.direct_h("You are a {}.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                if target.damage == 0:

                    # Hp is 0, prompt to receive 1 damage
                    data = {'options': ["Receive 1 damage"]}
                    target.ask_h('confirm', data, target.user_id)

                    # Give target 1 damage
                    new_damage = target.moveDamage(-1, args['self'])
                    target.gc.tell_h("{} took 1 damage!".format(target.user_id))

                else:

                    # Hp is nonzero, prompt to heal 1 damage
                    data = {'options': ["Heal 1 damage"]}
                    target.ask_h('confirm', data, target.user_id)

                    # Heal target 1 damage
                    new_damage = target.moveDamage(1, args['self'])
                    target.gc.tell_h("{} healed 1 damage!".format(target.user_id))

            else:

                # Target is not a shadow, nothing happens
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('confirm', data, target.user_id)
                target.gc.tell_h("{} did nothing.".format(target.user_id))

        def hermit_lesson(args):

            # Choose a player to give the card to
            args['self'].ask_h('confirm', {'options': ["Use Hermit's Lesson"]}, args['self'].user_id)
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            # If target's hp is >= 12, they take 2 damage.
            if target.character.max_damage >= 12:

                # Prompt target to receive 2 damage
                target.gc.direct_h("Your maximum hp ({}) is 12 or more.".format(target.character.max_damage), target.socket_id)
                data = {'options': ["Receive 2 damage"]}
                target.ask_h('confirm', data, target.user_id)

                # Give 2 damage to target
                new_damage = target.moveDamage(-2, args['self'])
                target.gc.tell_h("{} took 2 damage!".format(target.user_id))

            else:

                # Target's hp is < 12, nothing happens
                target.gc.direct_h("Your maximum hp is less than 12. Do nothing.".format(target.character.max_damage), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('confirm', data, target.user_id)
                target.gc.tell_h("{} did nothing.".format(target.user_id))

        def hermit_bully(args):

            # Choose a player to give the card to
            args['self'].ask_h('confirm', {'options': ["Use Hermit's Bully"]}, args['self'].user_id)
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            # If target's hp is <= 11, they take 1 damage.
            if target.character.max_damage <= 11:

                # Prompt target to receive 1 damage
                target.gc.direct_h("Your maximum hp ({}) is 11 or less.".format(target.character.max_damage), target.socket_id)
                data = {'options': ["Receive 1 damage"]}
                target.ask_h('confirm', data, target.user_id)

                # Give 1 damage to target
                new_damage = target.moveDamage(-1, args['self'])
                target.gc.tell_h("{} took 1 damage!".format(target.user_id))

            else:

                # Target's hp is > 11, nothing happens
                target.gc.direct_h("Your maximum hp is greater than 11. Do nothing.".format(target.character.max_damage), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('confirm', data, target.user_id)
                target.gc.tell_h("{} did nothing.".format(target.user_id))

        def hermit_prediction(args):

            # Choose a player to give the card to
            args['self'].ask_h('confirm', {'options': ["Use Hermit's Prediction"]}, args['self'].user_id)
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            # Prompt target to reveal themself
            target.gc.direct_h("You have no choice. Reveal yourself to {}.".format(args['self'].user_id), target.socket_id)
            data = {'options': ["Reveal"]}
            target.ask_h('confirm', data, target.user_id)

            # Send target's information to user
            target.gc.direct_h("{}\'s character is {}, a {} with {} hp.".format(
                target.user_id,
                target.character.name,
                ALLEGIANCE_MAP[target.character.alleg],
                target.character.max_damage
            ), args['self'].socket_id)
            target.gc.direct_h("Their win condition: {}.".format(target.character.win_cond_desc), args['self'].socket_id)
            target.gc.direct_h("Their special ability: {}.".format("None"), args['self'].socket_id)
            target.gc.tell_h("{} revealed their identity secretly to {}!".format(target.user_id, args['self'].user_id))

        ## Initialize hermit cards

        GREEN_CARDS = [
            card.Card(
                title = "Hermit\'s Blackmail",
                desc = ("I bet you're either a Neutral or a Hunter. "
                        "If so, you must either give an Equipment card to the current player or receive 1 damage!"),
                color = 2, # 2 : GREEN
                holder = None,
                is_equip = False,
                use = hermit_blackmail
            ),
            card.Card(
                title = "Hermit\'s Blackmail",
                desc = ("I bet you're either a Neutral or a Hunter. "
                        "If so, you must either give an Equipment card to the current player or receive 1 damage!"),
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_blackmail
            ),
            card.Card(
                title = "Hermit\'s Greed",
                desc = ("I bet you're either a Neutral or a Shadow. "
                        "If so, you must either give an Equipment card to the current player or receive 1 damage!"),
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_greed
            ),
            card.Card(
                title = "Hermit\'s Greed",
                desc = ("I bet you're either a Neutral or a Shadow. "
                        "If so, you must either give an Equipment card to the current player or receive 1 damage!"),
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_greed
            ),
            card.Card(
                title = "Hermit\'s Anger",
                desc = ("I bet you're either a Hunter or a Shadow. "
                        "If so, you must either give an Equipment card to the current player or receive 1 damage!"),
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_anger
            ),
            card.Card(
                title = "Hermit\'s Anger",
                desc = ("I bet you're either a Hunter or a Shadow. "
                        "If so, you must either give an Equipment card to the current player or receive 1 damage!"),
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_anger
            ),
            card.Card(
                title = "Hermit\'s Slap",
                desc = "I bet you're a Hunter. If so, you receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_slap
            ),
            card.Card(
                title = "Hermit\'s Slap",
                desc = "I bet you're a Hunter. If so, you receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_slap
            ),
            card.Card(
                title = "Hermit\'s Spell",
                desc = "I bet you're a Shadow. If so, you receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_spell
            ),
            card.Card(
                title = "Hermit\'s Exorcism",
                desc = "I bet you're a Shadow. If so, you receive 2 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_exorcism
            ),
            card.Card(
                title = "Hermit\'s Nurturance",
                desc = ("I bet you're a Neutral. If so, you heal 1 damage! "
                        "(However, if you have no damage, then you receive 1 damage!)"),
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_nurturance
            ),
            card.Card(
                title = "Hermit\'s Aid",
                desc = ("I bet you're a Hunter. If so, you heal 1 damage! "
                        "(However, if you have no damage, then you receive 1 damage!)"),
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_aid
            ),
            card.Card(
                title = "Hermit\'s Huddle",
                desc = ("I bet you're a Shadow. If so, you heal 1 damage! "
                        "(However, if you have no damage, then you receive 1 damage!)"),
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_huddle
            ),
            card.Card(
                title = "Hermit\'s Lesson",
                desc = "I bet your maximum HP is 12 or more. If so, you receive 2 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_lesson
            ),
            card.Card(
                title = "Hermit\'s Bully",
                desc = "I bet your maximum HP is 11 or less. If so, you receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_bully
            ),
            card.Card(
                title = "Hermit\'s Prediction",
                desc = "You must reveal your character information secretly to the current player!",
                color = 2,
                holder = None,
                is_equip = False,
                use = hermit_prediction
            )
        ]

        ## Initialize white, black, hermit decks

        self.WHITE_DECK = deck.Deck(cards = WHITE_CARDS)
        self.BLACK_DECK = deck.Deck(cards = BLACK_CARDS)
        self.GREEN_DECK = deck.Deck(cards = GREEN_CARDS)

        ## Character win condition functions

        def shadow_win_cond(gc, player):

            # Shadows win if all hunters are dead or 3 neutrals are dead
            no_living_hunters = (len([p for p in gc.getLivePlayers() if p.character.alleg == 2]) == 0)
            neutrals_dead_3 = (len([p for p in gc.getDeadPlayers() if p.character.alleg == 1]) >= 3)
            return no_living_hunters or neutrals_dead_3

        def hunter_win_cond(gc, player):

            # Hunters win if all shadows are dead
            no_living_shadows = (len([p for p in gc.getLivePlayers() if p.character.alleg == 0]) == 0)
            return no_living_shadows

        def allie_win_cond(gc, player):

            # Allie wins if she is still alive when the game ends
            return (player in gc.getLivePlayers()) and gc.game_over

        def bob_win_cond(gc, player):

            # Bob wins if he has 5+ equipment cards
            return len(player.equipment) >= 5

        def catherine_win_cond(gc, player):

            # Catherine wins if she is the first to die or one of the last 2 remaining
            first_to_die = (player in gc.getDeadPlayers()) and (len(gc.getDeadPlayers()) == 1)
            last_two = (player in gc.getLivePlayers()) and (len(gc.getLivePlayers()) <= 2)
            return first_to_die or last_two

        ## Specials
        def allie_special(gc, player):
            if !player.modifiers['special']:
                # Full heal
                player.setDamage(0, player)

                # Update modifiers
                player.modifiers['special'] = True

                # Tell
                gc.tell_h("Allie used her special ability: {}".format(player.character.special_desc))
            else:
                # Already used special
                gc.direct_h("This special ability can be used only once.", player.socket_id)

        ## Initialize characters

        self.CHARACTERS = [
            character.Character(
                name = "Valkyrie",
                alleg = 0,  # Shadow
                max_damage = 13,
                win_cond = shadow_win_cond,
                win_cond_desc = "All the Hunter characters are dead or 3 Neutral characters are dead",
                special = lambda: 0,  # TODO
                special_desc = "todo",
                resource_id = "valkyrie"
            ),
            character.Character(
                name = "Vampire",
                alleg = 0,  # Shadow
                max_damage = 13,
                win_cond = shadow_win_cond,
                win_cond_desc = "All the Hunter characters are dead or 3 Neutral characters are dead",
                special = lambda: 0,  # TODO
                special_desc = "todo",
                resource_id = "vampire"
            ),
            character.Character(
                name = "Werewolf",
                alleg = 0,  # Shadow
                max_damage = 14,
                win_cond = shadow_win_cond,
                win_cond_desc = "All the Hunter characters are dead or 3 Neutral characters are dead",
                special = lambda: 0,  # TODO
                special_desc = "todo",
                resource_id = "werewolf"
            ),
            character.Character(
                name = "Ultra Soul",
                alleg = 0,  # Shadow
                max_damage = 11,
                win_cond = shadow_win_cond,
                win_cond_desc = "All the Hunter characters are dead or 3 Neutral characters are dead",
                special = lambda: 0,  # TODO
                special_desc = "todo",
                resource_id = "vampire"
            ),
            character.Character(
                name = "Allie",
                alleg = 1,  # Neutral
                max_damage = 8,
                win_cond = allie_win_cond,
                win_cond_desc = "You're not dead when the game is over",
                special = lambda args: args[''],  # TODO
                special_desc = "Fully heal your damage",
                resource_id = "allie"
            ),
            character.Character(
                name = "Bob",
                alleg = 1,  # Neutral
                max_damage = 10,
                win_cond = bob_win_cond,
                win_cond_desc = "You have 5 or more equipment cards",
                special = lambda: 0,  # TODO
                special_desc = "todo",
                resource_id = "bob"
            ),
            character.Character(
                name = "Catherine",
                alleg = 1,  # Neutral
                max_damage = 11,
                win_cond = catherine_win_cond,
                win_cond_desc = "You are the first to die or you are one of the last two characters remaining",
                special = lambda: 0,  # TODO
                resource_id = "catherine"
            ),
            character.Character(
                name = "George",
                alleg = 2,  # Hunter
                max_damage = 14,
                win_cond = hunter_win_cond,
                win_cond_desc = "All the Shadow characters are dead",
                special = lambda: 0,  # TODO
                resource_id = "george"
            ),
            character.Character(
                name = "Fu-ka",
                alleg = 2,  # Hunter
                max_damage = 12,
                win_cond = hunter_win_cond,
                win_cond_desc = "All the Shadow characters are dead",
                special = lambda: 0,  # TODO
                resource_id = "fu-ka"
            ),
            character.Character(
                name = "Franklin",
                alleg = 2,  # Hunter
                max_damage = 12,
                win_cond = hunter_win_cond,
                win_cond_desc = "All the Shadow characters are dead",
                special = lambda: 0,  # TODO
                resource_id = "franklin"
            ),
            character.Character(
                name = "Ellen",
                alleg = 2,  # Hunter
                max_damage = 10,
                win_cond = hunter_win_cond,
                win_cond_desc = "All the Shadow characters are dead",
                special = lambda: 0,  # TODO
                resource_id = "ellen"
            )
        ]

        ## Area action functions

        def underworld_gate_action(gc, player):

            # Ask player which deck to draw from
            data = {'options': ["Draw White Card", "Draw Black Card", "Draw Hermit Card"]}
            answer = player.ask_h('select', data, player.user_id)['value']

            # Draw from corresponding deck
            if answer == "Draw White Card":
                player.drawCard(gc.white_cards)
            elif answer == "Draw Black Card":
                player.drawCard(gc.black_cards)
            else:
                player.drawCard(gc.green_cards)

        def weird_woods_action(gc, player):

            # Choose which player to attack or heal
            data = {'options': [p.user_id for p in gc.getLivePlayers()]}
            target = player.ask_h('select', data, player.user_id)['value']
            target_Player = [p for p in gc.getLivePlayers() if p.user_id == target][0]

            # Choose whether to attack or heal
            data = {'options': ["Heal 1 damage", "Give 2 damage"]}
            amount = player.ask_h('select', data, player.user_id)['value']
            if amount == "Heal 1 damage":
                target_Player.moveDamage(1, player)
            else:
                target_Player.moveDamage(-2, player)

        def erstwhile_altar_action(gc, player):

            # Get players who have equipment
            players_w_items = [p for p in gc.getLivePlayers() if (len(p.equipment) and p != player)]

            # If someone has equipment to steal and isn't current player, offer choice
            if len(players_w_items):

                # Choose player to steal from
                data = {'options': [p.user_id for p in players_w_items]}
                target = player.ask_h('select', data, player.user_id)['value']
                target_Player = [p for p in players_w_items if p.user_id == target][0]

                # Choose equipment to take from player
                data = {'options': [eq.title for eq in target_Player.equipment]}
                equip = player.ask_h('select', data, player.user_id)['value']
                equip_Equipment = [eq for eq in target_Player.equipment if eq.title == equip][0]

                # Transfer equipment from one player to the other
                i = target_Player.equipment.index(equip_Equipment)
                equip_Equipment = target_Player.equipment.pop(i)
                player.equipment.append(equip_Equipment)
                equip_Equipment.holder = player
                gc.tell_h("{} stole {}'s {}!".format(player.user_id, target_Player.user_id, equip_Equipment.title))

                # Update frontend with transfer
                gc.update_h()

            else:

                # If no one has equipment to steal, nothing happens
                gc.tell_h("Nobody has any items for {} to steal.".format(player.user_id))

        ## Initialize areas

        self.AREAS = [
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
                action = erstwhile_altar_action,
                resource_id = "erstwhile-altar"
            )
        ]
