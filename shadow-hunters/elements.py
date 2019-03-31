import card, deck, character, area

# elements.py
# Encodes all characters, win conditions, special abilities,
# game areas, decks, and cards in an element factory. Every
# game context is initialized with its own element factory.

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

class ElementFactory:
    def __init__(self):

        # Helper functions for asking players to make choices
        def choose_player(args):
            args['self'].gc.tell_h("{} is choosing a player...".format(args['self'].user_id))
            data = {'options': [p.user_id for p in args['self'].gc.getLivePlayers() if p != args['self']]}
            target = args['self'].ask_h('select', data, args['self'].user_id)['value']
            args['self'].gc.update_h()
            target_Player = [p for p in args['self'].gc.getLivePlayers() if p.user_id == target][0]
            args['self'].gc.tell_h("{} chose {}!".format(args['self'].user_id, target))
            return target_Player

        def choose_equipment(player, target):
            data = {'options': [eq.title for eq in target.equipment]}
            equip = target.ask_h('select', data, player.user_id)['value']
            player.gc.update_h()
            equip_Equipment = [eq for eq in target.equipment if eq.title == equip][0]
            return equip_Equipment

        # White card usage functions
        def use_first_aid(args):
            target = args['self'].ask_h('select', {'options': [t.user_id for t in args['self'].gc.getLivePlayers()]}, args['self'].user_id)['value']
            args['self'].gc.update_h()
            [p for p in args['self'].gc.getLivePlayers() if p.user_id == target][0].setDamage(7)
            args['self'].gc.update_h()

        def use_advent(args):
            raise NotImplementedError

        def use_disenchant_mirror(args):
            raise NotImplementedError

        def use_blessing(args):
            raise NotImplementedError

        def use_chocolate(args):
            raise NotImplementedError

        def use_concealed_knowledge(args):
            raise NotImplementedError

        def use_guardian_angel(args):
            raise NotImplementedError

        # Initialize white cards
        WHITE_CARDS = [
            card.Card(
                title = "Holy Robe",
                desc = "Your attacks do 1 less damage and the amount of damage you receive from attacks is reduced by 1 point.",
                color = 0, # 0 : WHITE
                holder = None,
                is_equip = True,
                force_use = False,
                use = lambda is_attack, successful, amt: max(0, amt - 1) # applies to both attack and defend
            ),
            card.Card(
                title = "Flare of Judgement",
                desc = "All characters except yourself receive 2 points of damage.",
                color = 0,
                holder = None,
                is_equip = False,
                force_use = True,
                use = lambda args: [p.moveDamage(-2) for p in args['self'].gc.getLivePlayers() if p != args['self']]
            ),
            card.Card(
                title = "First Aid",
                desc = "Place a character's damage marker to 7 (You can choose yourself).",
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
                use = lambda args: args['self'].moveDamage(2)
            ),
            card.Card(
                title = "Holy Water of Healing",
                desc = "Heal 2 points of your damage.",
                color = 0,
                holder = None,
                is_equip = False,
                force_use = True,
                use = lambda args: args['self'].moveDamage(2)
            )
        ]

        # Black card usage functions
        def use_bloodthirsty_spider(args):
            target = choose_player(args)
            args['self'].gc.update_h()
            target.moveDamage(-2)
            args['self'].moveDamage(-2)
            args['self'].gc.update_h()

        def use_vampire_bat(args):
            target = choose_player(args)
            args['self'].gc.update_h()
            target.moveDamage(-2)
            args['self'].moveDamage(1)
            args['self'].gc.update_h()

        def use_moody_goblin(args):
            players_w_items = [p for p in args['self'].gc.getLivePlayers() if (len(p.equipment) and p != args['self'])]
            if len(players_w_items):
                data = {'options': [p.user_id for p in players_w_items]}
                target = args['self'].ask_h('select', data, args['self'].user_id)['value']
                args['self'].gc.update_h()
                target_Player = [p for p in args['self'].gc.getLivePlayers() if p.user_id == target][0]
                data = {'options': [eq.title for eq in target_Player.equipment]}
                equip = args['self'].ask_h('select', data, args['self'].user_id)['value']
                args['self'].gc.update_h()
                equip_Equipment = [eq for eq in target_Player.equipment if eq.title == equip][0]

                i = target_Player.equipment.index(equip_Equipment)
                equip_Equipment = target_Player.equipment.pop(i)
                args['self'].equipment.append(equip_Equipment)
                equip_Equipment.holder = args['self']
                args['self'].gc.tell_h("{} stole {}'s {}!".format(args['self'].user_id, target_Player.user_id, equip_Equipment.title))
                args['self'].gc.update_h()
            else:
                args['self'].gc.tell_h("Nobody has any items for {} to steal.".format(args['self'].user_id))
            args['self'].gc.update_h()

        def use_diabolic_ritual(args):
            data = {'options': ["Do nothing"]}
            if args['self'].character.alleg == 0:
                data['options'].append("Reveal and heal fully")
            decision = args['self'].ask_h('select', data, args['self'].user_id)['value']
            if decision == "Do nothing":
                args['self'].gc.tell_h("{} did nothing.".format(args['self'].user_id))
            else:
                args['self'].reveal()
                args['self'].setDamage(0)
            args['self'].gc.update_h()

        def use_banana_peel(args):
            if len(args['self'].equipment):
                data = {'options': ["Give an equipment card", "Receive 1 damage"]}
            else:
                data = {'options': ["Receive 1 damage"]}
            decision = args['self'].ask_h('select', data, args['self'].user_id)['value']
            args['self'].gc.update_h()
            if decision == "Give an equipment card":
                args['self'].gc.tell_h("{} is choosing an equipment card to give away...".format(args['self'].user_id))
                eq = choose_equipment(args['self'], args['self'])
                receiver = choose_player(args)
                i = args['self'].equipment.index(eq)
                eq = args['self'].equipment.pop(i)
                receiver.equipment.append(eq)
                eq.holder = receiver
                args['self'].gc.tell_h("{} gave {} their {}!".format(args['self'].user_id, receiver.user_id, eq.title))
            else:
                args['self'].moveDamage(-1)
            args['self'].gc.update_h()

        def use_dynamite(args):
            args['self'].gc.tell_h("{} is rolling for location...".format(args['self'].user_id))
            data = {'options': ['Roll for location']}
            args['self'].ask_h('confirm', data, args['self'].user_id)
            roll_result_4 = args['self'].gc.die4.roll()
            roll_result_6 = args['self'].gc.die6.roll()
            roll_result = roll_result_4 + roll_result_6
            args['self'].gc.tell_h("{} rolled {} + {} = {}!".format(args['self'].user_id, roll_result_4, roll_result_6, roll_result))
            args['self'].gc.update_h()

            if roll_result == 7:
                args['self'].gc.tell_h("Nothing happens.")
            else:
                destination_Area = None
                for z in args['self'].gc.zones:
                    for a in z.areas:
                        if roll_result in a.domain:
                            destination_Area = a
                destination = destination_Area.name
                args['self'].gc.tell_h("Dynamite blew up the {}!".format(destination))
                affected_players = [p for p in args['self'].gc.players if p.location == destination_Area]
                for p in affected_players:
                    p.moveDamage(-3)
            args['self'].gc.update_h()

        def use_spiritual_doll(args):
            target = choose_player(args)
            args['self'].gc.update_h()
            args['self'].gc.tell_h("{} is rolling the 6-sided die...".format(args['self'].user_id))
            data = {'options': ['Roll the 6-sided die']}
            args['self'].ask_h('confirm', data, args['self'].user_id)
            roll_result = args['self'].gc.die6.roll()
            args['self'].gc.tell_h("{} rolled a {}!".format(args['self'].user_id, roll_result))
            if roll_result >= 5:
                args['self'].moveDamage(-3)
            else:
                target.moveDamage(-3)
            args['self'].gc.update_h()

        # Initialize black cards
        BLACK_CARDS = [
            card.Card(
                title = "Butcher Knife",
                desc = "If your attack is successful, you give 1 point of extra damage.",
                color = 1, # 1 : BLACK
                holder = None,
                is_equip = True,
                force_use = False,
                use = lambda is_attack, successful, amt: amt + 1 if (is_attack and successful) else amt
            ),
            card.Card(
                title = "Chainsaw",
                desc = "If your attack is successful, you give 1 point of extra damage.",
                color = 1,
                holder = None,
                is_equip = True,
                force_use = False,
                use = lambda is_attack, successful, amt: amt + 1 if (is_attack and successful) else amt
            ),
            card.Card(
                title = "Rusted Broad Axe",
                desc = "If your attack is successful, you give 1 point of extra damage.",
                color = 1,
                holder = None,
                is_equip = True,
                force_use = False,
                use = lambda is_attack, successful, amt: amt + 1 if (is_attack and successful) else amt
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
            ),
            card.Card(
                title = "Diabolic Ritual",
                desc = "If you are a Shadow, you may reveal your identity. If you do, you fully heal you damage.",
                color = 1,
                holder = None,
                is_equip = False,
                force_use = True,
                use = use_diabolic_ritual
            ),
            card.Card(
                title = "Banana Peel",
                desc = "Give one of your equipment cards to another character. If you have no equipment cards, you receive 1 point of damage.",
                color = 1,
                holder = None,
                is_equip = False,
                force_use = True,
                use = use_banana_peel
            ),
            card.Card(
                title = "Dynamite",
                desc = "Roll 2 dice and give 3 points of damage to all characters in the area designated by the total number rolled (nothing happens if a 7 is rolled).",
                color = 1,
                holder = None,
                is_equip = False,
                force_use = True,
                use = use_dynamite
            ),
            card.Card(
                title = "Spiritual Doll",
                desc = "Pick a character and roll the 6-sided die. If the die number is 1 to 4, you give 3 points of damage to that character. If the die number is 5 or 6, you get 3 points of damage.",
                color = 1,
                holder = None,
                is_equip = False,
                force_use = True,
                use = use_spiritual_doll
            )
        ]

        # Hermit card usage functions
        def hermit_blackmail(args):
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            if target.character.alleg > 0: ## neutral or hunter
                target.gc.direct_h("You are a {}. Make a choice.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                if len(target.equipment):
                    data = {'options': ["Give an equipment card", "Receive 1 damage"]}
                else:
                    data = {'options': ["Receive 1 damage"]}
                decision = target.ask_h('select', data, target.user_id)['value']
                target.gc.update_h()
                if decision == "Give an equipment card":
                    target.gc.tell_h("{} is choosing an equipment card to give to {}...".format(target.user_id, args['self'].user_id))
                    eq = choose_equipment(target, target)
                    i = target.equipment.index(eq)
                    eq = target.equipment.pop(i)
                    args['self'].equipment.append(eq)
                    eq.holder = args['self']
                    args['self'].gc.tell_h("{} gave {} their {}!".format(target.user_id, args['self'].user_id, eq.title))
                else:
                    new_damage = target.moveDamage(-1)
                    target.gc.tell_h("{}\'s damage is now {}!".format(target.user_id, new_damage))

            else:
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('yesno', data, target.user_id)['value']
                target.gc.update_h()
                target.gc.tell_h("{} did nothing.".format(target.user_id))
            target.gc.update_h()

        def hermit_greed(args):
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            if target.character.alleg < 2: ## neutral or shadow
                target.gc.direct_h("You are a {}. Make a choice.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                if len(target.equipment):
                    data = {'options': ["Give an equipment card", "Receive 1 damage"]}
                else:
                    data = {'options': ["Receive 1 damage"]}
                decision = target.ask_h('select', data, target.user_id)['value']
                target.gc.update_h()
                if decision == "Give an equipment card":
                    target.gc.tell_h("{} is choosing an equipment card to give to {}...".format(target.user_id, args['self'].user_id))
                    eq = choose_equipment(target, target)
                    i = target.equipment.index(eq)
                    eq = target.equipment.pop(i)
                    args['self'].equipment.append(eq)
                    eq.holder = args['self']
                    args['self'].gc.tell_h("{} gave {} their {}!".format(target.user_id, args['self'].user_id, eq.title))
                else:
                    new_damage = target.moveDamage(-1)
                    target.gc.tell_h("{}\'s damage is now {}!".format(target.user_id, new_damage))
            else:
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('yesno', data, target.user_id)['value']
                target.gc.update_h()
                target.gc.tell_h("{} did nothing.".format(target.user_id))
            target.gc.update_h()

        def hermit_anger(args):
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            if target.character.alleg in [0, 2]: ## hunter or shadow
                target.gc.direct_h("You are a {}. Make a choice.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                if len(target.equipment):
                    data = {'options': ["Give an equipment card", "Receive 1 damage"]}
                else:
                    data = {'options': ["Receive 1 damage"]}
                decision = target.ask_h('select', data, target.user_id)['value']
                target.gc.update_h()
                if decision == "Give an equipment card":
                    target.gc.tell_h("{} is choosing an equipment card to give to {}...".format(target.user_id, args['self'].user_id))
                    eq = choose_equipment(target, target)
                    i = target.equipment.index(eq)
                    eq = target.equipment.pop(i)
                    args['self'].equipment.append(eq)
                    eq.holder = args['self']
                    args['self'].gc.tell_h("{} gave {} their {}!".format(target.user_id, args['self'].user_id, eq.title))
                else:
                    new_damage = target.moveDamage(-1)
                    target.gc.tell_h("{}'s damage is now {}!".format(target.user_id, new_damage))
            else:
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('yesno', data, target.user_id)['value']
                target.gc.update_h()
                target.gc.tell_h("{} did nothing.".format(target.user_id))
            target.gc.update_h()

        def hermit_slap(args):
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            if target.character.alleg == 2: ## hunter
                target.gc.direct_h("You are a {}.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ["Receive 1 damage"]}
                target.ask_h('select', data, target.user_id)['value']
                target.gc.update_h()
                new_damage = target.moveDamage(-1)
                target.gc.tell_h("{}\'s Damage is now {}!".format(target.user_id, new_damage))
            else:
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('yesno', data, target.user_id)['value']
                target.gc.update_h()
                target.gc.tell_h("{} did nothing.".format(target.user_id))
            target.gc.update_h()

        def hermit_spell(args):
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            if target.character.alleg == 0: ## shadow
                target.gc.direct_h("You are a {}.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ["Receive 1 damage"]}
                target.ask_h('select', data, target.user_id)['value']
                target.gc.update_h()
                new_damage = target.moveDamage(-1)
                target.gc.tell_h("{}\'s damage is now {}!".format(target.user_id, new_damage))
            else:
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('yesno', data, target.user_id)['value']
                target.gc.update_h()
                target.gc.tell_h("{} did nothing.".format(target.user_id))
            target.gc.update_h()

        def hermit_exorcism(args):
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            if target.character.alleg == 0: ## shadow
                target.gc.direct_h("You are a {}.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ["Receive 2 damage"]}
                target.ask_h('select', data, target.user_id)['value']
                target.gc.update_h()
                new_damage = target.moveDamage(-2)
                target.gc.tell_h("{}\'s damage is now {}!".format(target.user_id, new_damage))
            else:
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('yesno', data, target.user_id)['value']
                target.gc.update_h()
                target.gc.tell_h("{} did nothing.".format(target.user_id))
            target.gc.update_h()

        def hermit_nurturance(args):
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            if target.character.alleg == 1: ## neutral
                target.gc.direct_h("You are a {}.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                if target.damage == 0:
                    data = {'options': ["Receive 1 damage"]}
                    target.ask_h('select', data, target.user_id)['value']
                    target.gc.update_h()
                    new_damage = target.moveDamage(-1)
                else:
                    data = {'options': ["Heal 1 damage"]}
                    target.ask_h('select', data, target.user_id)['value']
                    target.gc.update_h()
                    new_damage = target.moveDamage(1)
                target.gc.tell_h("{}\'s damage is now {}!".format(target.user_id, new_damage))
            else:
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('yesno', data, target.user_id)['value']
                target.gc.update_h()
                target.gc.tell_h("{} did nothing.".format(target.user_id))
            target.gc.update_h()

        def hermit_aid(args):
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            if target.character.alleg == 2: ## hunter
                target.gc.direct_h("You are a {}.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                if target.damage == 0:
                    data = {'options': ["Receive 1 damage"]}
                    target.ask_h('select', data, target.user_id)['value']
                    target.gc.update_h()
                    new_damage = target.moveDamage(-1)
                else:
                    data = {'options': ["Heal 1 damage"]}
                    target.ask_h('select', data, target.user_id)['value']
                    target.gc.update_h()
                    new_damage = target.moveDamage(1)
                target.gc.tell_h("{}\'s damage is now {}!".format(target.user_id, new_damage))
            else:
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('yesno', data, target.user_id)['value']
                target.gc.update_h()
                target.gc.tell_h("{} did nothing.".format(target.user_id))
            target.gc.update_h()

        def hermit_huddle(args):
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            if target.character.alleg == 0: ## shadow
                target.gc.direct_h("You are a {}.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                if target.damage == 0:
                    data = {'options': ["Receive 1 damage"]}
                    target.ask_h('select', data, target.user_id)['value']
                    target.gc.update_h()
                    new_damage = target.moveDamage(-1)
                else:
                    data = {'options': ["Heal 1 damage"]}
                    target.ask_h('select', data, target.user_id)['value']
                    target.gc.update_h()
                    new_damage = target.moveDamage(1)
                target.gc.tell_h("{}\'s damage is now {}!".format(target.user_id, new_damage))
            else:
                target.gc.direct_h("You are a {}. Do nothing.".format(ALLEGIANCE_MAP[target.character.alleg]), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('yesno', data, target.user_id)['value']
                target.gc.update_h()
                target.gc.tell_h("{} did nothing.".format(target.user_id))
            target.gc.update_h()

        def hermit_lesson(args):
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            if target.character.max_damage >= 12:
                target.gc.direct_h("Your maximum hp ({}) is 12 or more.".format(target.character.max_damage), target.socket_id)
                data = {'options': ["Receive 2 damage"]}
                target.ask_h('select', data, target.user_id)['value']
                target.gc.update_h()
                new_damage = target.moveDamage(-2)
                target.gc.tell_h("{}\'s Damage is now {}!".format(target.user_id, new_damage))
            else:
                target.gc.direct_h("Your maximum hp ({}) is less than 12. Do nothing.".format(target.character.max_damage), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('yesno', data, target.user_id)['value']
                target.gc.update_h()
                target.gc.tell_h("{} did nothing.".format(target.user_id))
            target.gc.update_h()

        def hermit_bully(args):
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)

            if target.character.max_damage <= 11:
                target.gc.direct_h("Your maximum hp ({}) is 11 or less.".format(target.character.max_damage), target.socket_id)
                data = {'options': ["Receive 1 damage"]}
                target.ask_h('select', data, target.user_id)['value']
                target.gc.update_h()
                new_damage = target.moveDamage(-1)
                target.gc.tell_h("{}\'s Damage is now {}!".format(target.user_id, new_damage))
            else:
                target.gc.direct_h("Your maximum hp ({}) is greater than 11. Do nothing.".format(target.character.max_damage), target.socket_id)
                data = {'options': ['Do nothing']}
                target.ask_h('yesno', data, target.user_id)['value']
                target.gc.update_h()
                target.gc.tell_h("{} did nothing.".format(target.user_id))
            target.gc.update_h()

        def hermit_prediction(args):
            target = choose_player(args)
            args['self'].gc.direct_h("{} says: {}".format(args['self'].user_id, args['card'].desc), target.socket_id)
            target.gc.direct_h("You have no choice. Reveal yourself to {}.".format(args['self'].user_id), target.socket_id)
            data = {'options': ["Send your character information"]}
            target.ask_h('select', data, target.user_id)['value']
            target.gc.direct_h("{}\'s character is {}, a {} with {} hp.".format(
                target.user_id,
                target.character.name,
                ALLEGIANCE_MAP[target.character.alleg],
                target.character.max_damage
            ), args['self'].socket_id)
            target.gc.direct_h("Their win condition: {}.".format(target.character.win_cond_desc), args['self'].socket_id)
            target.gc.direct_h("Their special ability: {}.".format("None"), args['self'].socket_id)
            target.gc.tell_h("{} revealed their identity secretly to {}!".format(target.user_id, args['self'].user_id))
            target.gc.update_h()

        # Initialize hermit cards
        GREEN_CARDS = [
            card.Card(
                title = "Hermit\'s Blackmail",
                desc = "I bet you're either a Neutral or a Hunter. If so, you must either give an Equipment card to the current player or receive 1 damage!",
                color = 2, # 2 : GREEN
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_blackmail
            ),
            card.Card(
                title = "Hermit\'s Blackmail",
                desc = "I bet you're either a Neutral or a Hunter. If so, you must either give an Equipment card to the current player or receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_blackmail
            ),
            card.Card(
                title = "Hermit\'s Greed",
                desc = "I bet you're either a Neutral or a Shadow. If so, you must either give an Equipment card to the current player or receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_greed
            ),
            card.Card(
                title = "Hermit\'s Greed",
                desc = "I bet you're either a Neutral or a Shadow. If so, you must either give an Equipment card to the current player or receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_greed
            ),
            card.Card(
                title = "Hermit\'s Anger",
                desc = "I bet you're either a Hunter or a Shadow. If so, you must either give an Equipment card to the current player or receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_anger
            ),
            card.Card(
                title = "Hermit\'s Anger",
                desc = "I bet you're either a Hunter or a Shadow. If so, you must either give an Equipment card to the current player or receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_anger
            ),
            card.Card(
                title = "Hermit\'s Slap",
                desc = "I bet you're a Hunter. If so, you receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_slap
            ),
            card.Card(
                title = "Hermit\'s Slap",
                desc = "I bet you're a Hunter. If so, you receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_slap
            ),
            card.Card(
                title = "Hermit\'s Spell",
                desc = "I bet you're a Shadow. If so, you receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_spell
            ),
            card.Card(
                title = "Hermit\'s Exorcism",
                desc = "I bet you're a Shadow. If so, you receive 2 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_exorcism
            ),
            card.Card(
                title = "Hermit\'s Nurturance",
                desc = "I bet you're a Neutral. If so, you heal 1 damage! (However, if you have no damage, then you receive 1 damage!)",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_nurturance
            ),
            card.Card(
                title = "Hermit\'s Aid",
                desc = "I bet you're a Hunter. If so, you heal 1 damage! (However, if you have no damage, then you receive 1 damage!)",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_aid
            ),
            card.Card(
                title = "Hermit\'s Huddle",
                desc = "I bet you're a Shadow. If so, you heal 1 damage! (However, if you have no damage, then you receive 1 damage!)",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_huddle
            ),
            card.Card(
                title = "Hermit\'s Lesson",
                desc = "I bet your maximum HP is 12 or more. If so, you receive 2 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_lesson
            ),
            card.Card(
                title = "Hermit\'s Bully",
                desc = "I bet your maximum HP is 11 or less. If so, you receive 1 damage!",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_bully
            ),
            card.Card(
                title = "Hermit\'s Prediction",
                desc = "You must reveal your character information secretly to the current player!",
                color = 2,
                holder = None,
                is_equip = False,
                force_use = True,
                use = hermit_prediction
            )
        ]

        # Initialize white, black, hermit decks
        self.WHITE_DECK = deck.Deck(cards = WHITE_CARDS)
        self.BLACK_DECK = deck.Deck(cards = BLACK_CARDS)
        self.GREEN_DECK = deck.Deck(cards = GREEN_CARDS)

        # Character win condition functions
        def shadow_win_cond(gc, player):
            no_living_hunters = (len([p for p in gc.getLivePlayers() if p.character.alleg == 2]) == 0)
            neutrals_dead_3 = (len([p for p in gc.getDeadPlayers() if p.character.alleg == 1]) >= 3)
            return no_living_hunters or neutrals_dead_3

        def hunter_win_cond(gc, player):
            no_living_shadows = (len([p for p in gc.getLivePlayers() if p.character.alleg == 0]) == 0)
            return no_living_shadows

        def allie_win_cond(gc, player):
            return (player in gc.getLivePlayers()) and gc.game_over

        # Initialize characters
        self.CHARACTERS = [
            character.Character(
                name = "Valkyrie",
                alleg = 0,  # Shadow
                max_damage = 13,
                win_cond = shadow_win_cond,
                win_cond_desc = "All the Hunter characters are dead or 3 Neutral characters are dead",
                special = lambda: 0,  # TODO
                resource_id = "valkyrie"
            ),
            character.Character(
                name = "Vampire",
                alleg = 0,  # Shadow
                max_damage = 13,
                win_cond = shadow_win_cond,
                win_cond_desc = "All the Hunter characters are dead or 3 Neutral characters are dead",
                special = lambda: 0,  # TODO
                resource_id = "vampire"
            ),
            character.Character(
                name = "Allie",
                alleg = 1,  # Neutral
                max_damage = 8,
                win_cond = allie_win_cond,
                win_cond_desc = "You're not dead when the game is over",
                special = lambda: 0,  # TODO
                resource_id = "allie"
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
            )
        ]

        # Area action functions
        def underworld_gate_action(gc, player):
            data = {'options': ["Draw White Card", "Draw Black Card", "Draw Hermit Card"]}
            answer = player.ask_h('select', data, player.user_id)['value']
            gc.update_h()
            if answer == "Draw White Card":
                player.drawCard(gc.white_cards)
            elif answer == "Draw Black Card":
                player.drawCard(gc.black_cards)
            else:
                player.drawCard(gc.green_cards)
            gc.update_h()

        def weird_woods_action(gc, player):
            data = {'options': [p.user_id for p in gc.getLivePlayers()]}
            target = player.ask_h('select', data, player.user_id)['value']
            gc.update_h()
            target_Player = [p for p in gc.getLivePlayers() if p.user_id == target][0]

            data = {'options': ["Heal 1 damage", "Give 2 damage"]}
            amount = player.ask_h('select', data, player.user_id)['value']
            gc.update_h()
            if amount == "Heal 1 damage":
                target_Player.moveDamage(1)
            else:
                target_Player.moveDamage(-2)
            gc.update_h()

        def erstwhile_altar_action(gc, player):
            players_w_items = [p for p in gc.getLivePlayers() if (len(p.equipment) and p != player)]
            if len(players_w_items):
                data = {'options': [p.user_id for p in players_w_items]}
                target = player.ask_h('select', data, player.user_id)['value']
                gc.update_h()
                target_Player = [p for p in players_w_items if p.user_id == target][0]

                data = {'options': [eq.title for eq in target_Player.equipment]}
                equip = player.ask_h('select', data, player.user_id)['value']
                gc.update_h()
                equip_Equipment = [eq for eq in target_Player.equipment if eq.title == equip][0]

                i = target_Player.equipment.index(equip_Equipment)
                equip_Equipment = target_Player.equipment.pop(i)
                player.equipment.append(equip_Equipment)
                equip_Equipment.holder = player
                gc.tell_h("{} stole {}'s {}!".format(player.user_id, target_Player.user_id, equip_Equipment.title))
            else:
                gc.tell_h("Nobody has any items for {} to steal.".format(player.user_id))
            gc.update_h()

        # Initialize areas
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
