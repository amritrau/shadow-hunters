import elements
from collections import defaultdict

class Player:
    def __init__(self, user_id, socket_id, ask_h, ai):
        self.user_id = user_id
        self.socket_id = socket_id
        self.gc = None # game context (abbreviated for convenience)
        self.state = 2 #  2 for ALIVE_ANON, 1 for ALIVE_KNOWN, 0 for DEAD
        self.character = None
        self.equipment = []
        self.damage = 0
        self.location = None
        self.modifiers = defaultdict(lambda: False)
        self.modifiers['attack_dice_type'] = "attack"
        self.ask_h = ask_h
        self.ai = ai

    def setCharacter(self, character):
        self.character = character

    def reveal(self):

        # Set state
        self.state = 1

        # Reveal character to frontend
        self.gc.update_h()

        # Broadcast reveal
        display_data = {'type': 'reveal', 'player': self.dump()}
        self.gc.show_h(display_data)
        self.gc.tell_h("{} revealed themselves as {}, a {} with {} hp!".format(
            self.user_id,
            self.character.name,
            elements.ALLEGIANCE_MAP[self.character.alleg],
            self.character.max_damage
        ))
        self.gc.tell_h("Their win condition: {}.".format(self.character.win_cond_desc))
        self.gc.tell_h("Their special ability: {}.".format("None"))

    def takeTurn(self):
        # Before turn check for special ability
        if self.modifiers['special_active']:
            self.character.special(self.gc, self, turn_pos = 'start')

        # takeTurn
        self._takeTurn()

        # After turn check for special ability
        if self.modifiers['special_active']:
            self.character.special(self.gc, self, turn_pos = 'end')

    def _takeTurn(self):

        # Announce player
        self.gc.tell_h("It's {}'s turn!".format(self.user_id))

        # Guardian Angel wears off
        if "guardian_angel" in self.modifiers:
            self.gc.tell_h("The effect of {}\'s Guardian Angel wore off!".format(self.user_id))
            del self.modifiers["guardian_angel"]

        # Roll dice
        self.gc.tell_h("{} is rolling for movement...".format(self.user_id))
        roll_result = self.rollDice('area')

        if "Mystic Compass" in [e.title for e in self.equipment]:

            # If player has mystic compass, roll again
            self.gc.tell_h("{}'s Mystic Compass lets them roll again!".format(self.user_id))
            second_roll = self.rollDice('area')

            # Pick the preferred roll
            data = {'options': ["Use {}".format(roll_result), "Use {}".format(second_roll)]}
            answer = self.ask_h('yesno', data, self.user_id)['value']
            roll_result = int(answer[4:])

        # Figure out area to move to
        if roll_result == 7:

            # Select an area
            self.gc.tell_h("{} is selecting an area...".format(self.user_id))
            area_options = []
            for z in self.gc.zones:
                for a in z.areas:
                    area_options.append(a.name)
            data = {'options': area_options}
            destination = self.ask_h('select', data, self.user_id)['value']

            # Get Area object from area name
            destination_Area = None
            for z in self.gc.zones:
                for a in z.areas:
                    if a.name == destination:
                        destination_Area = a

        else:

            # Get area from roll
            destination_Area = None
            for z in self.gc.zones:
                for a in z.areas:
                    if roll_result in a.domain:
                        destination_Area = a

            # Get string from area
            destination = destination_Area.name

        # Move to area
        self.move(destination_Area)
        self.gc.tell_h("{} moves to {}!".format(self.user_id, destination))

        # Take area action
        data = {'options': [destination_Area.desc, 'Decline']}
        answer = self.ask_h('yesno', data, self.user_id)['value']
        if answer != 'Decline':
            self.location.action(self.gc, self)
        else:
            self.gc.tell_h('{} declined to perform their area action.'.format(self.user_id))

        # Someone could have died here, so check win conditions
        if self.gc.checkWinConditions(tell = False):
            return  # let the win conditions check in GameContext.play() handle

        # The current player could have died -- if so end their turn
        if self.state == 0:
            return

        # Attack
        self.attackSequence(dice_type = self.modifiers['attack_dice_type'])

        # The current player could have died -- if so end their turn
        if self.state == 0:
            return

        # Turn is over
        self.gc.tell_h("{}'s turn is over.".format(self.user_id))

    def attackSequence(self, dice_type = "attack"):
        self.ask_h('confirm', {'options': ["Attack other players!"]}, self.user_id)
        self.gc.tell_h("{} is picking whom to attack...".format(self.user_id))

        # Get attackable players
        live_players = [p for p in self.gc.getLivePlayers() if p.location]
        targets = [p for p in live_players if (p.location.zone == self.location.zone and p != self)]
        if "Handgun" in [e.title for e in self.equipment]:
            self.gc.tell_h("{}'s Handgun reverses their attack range.".format(self.user_id))
            targets = [p for p in live_players if (p.location.zone != self.location.zone and p != self)]

        # If player has Muramasa, can't decline unless there are no options
        # TODO is this a bug?
        data = {'options': [t.user_id for t in targets]}
        if ("Cursed Sword Masamune" not in [e.title for e in self.equipment]) or len(data['options']) == 0:
            data['options'].append("Decline")
        answer = self.ask_h('select', data, self.user_id)['value']

        if answer != 'Decline':

            # Get target
            target_name = answer
            target_Player = [p for p in self.gc.getLivePlayers() if p.user_id == target_name][0]
            self.gc.tell_h("{} is attacking {}!".format(self.user_id, target_name))

            # Roll with the 4-sided die if the player has masamune
            roll_result = 0
            if "Cursed Sword Masamune" in [e.title for e in self.equipment]:
                self.gc.tell_h("{} rolls with the 4-sided die using the Masamune!".format(self.user_id, roll_result))
                roll_result = self.rollDice('4')
            else:
                roll_result = self.rollDice(dice_type)

            # If player has Machine Gun, launch attack on everyone in the zone. Otherwise, attack the target
            if "Machine Gun" in [e.title for e in self.equipment]:
                self.gc.tell_h("{}'s Machine Gun hits everyone in their attack range!".format(self.user_id))
                for t in targets:
                    damage_dealt = self.attack(t, roll_result)
                    self.gc.tell_h("{} hit {} for {} damage!".format(self.user_id, t.user_id, damage_dealt))
            else:
                damage_dealt = self.attack(target_Player, roll_result)
                self.gc.tell_h("{} hit {} for {} damage!".format(self.user_id, target_name, damage_dealt))
        else:
            self.gc.tell_h("{} declined to attack.".format(self.user_id))

    def drawCard(self, deck):

        # Draw card and tell frontend about it
        drawn = deck.drawCard()
        public_title = drawn.title if drawn.color != 2 else 'a Hermit Card'
        self.gc.tell_h("{} drew {}!".format(self.user_id, public_title))
        display_data = drawn.dump()
        display_data['type'] = 'draw'
        if drawn.color != 2:
            self.gc.tell_h("{}: {}".format(drawn.title, drawn.desc))
            self.gc.show_h(display_data)
        else:
            self.gc.tell_h("{}: {}".format(drawn.title, drawn.desc), client=self.socket_id)
            self.gc.show_h(display_data, client=self.socket_id)

        # Use card if it's single-use, or add to arsenal if it's equipment
        if drawn.is_equipment:
            self.ask_h('confirm', {'options': ["Add {} to arsenal".format(drawn.title)]}, self.user_id)
            self.gc.tell_h("{} added {} to their arsenal!".format(self.user_id, public_title))
            self.equipment.append(drawn)
            self.gc.update_h()
        else:
            args = {'self': self, 'card': drawn}
            drawn.use(args)

    def rollDice(self, type):

        # Preprocess all rolls
        assert type in ["area", "attack", "6", "4"]
        roll_4 = self.gc.die4.roll()
        roll_6 = self.gc.die6.roll()
        diff = abs(roll_4 - roll_6)
        sum = roll_4 + roll_6

        # Set values based on type of roll
        if type == "area":
            ask_data = {'options': ['Roll the dice!']}
            display_data = {'type': 'roll', '4-sided': roll_4, '6-sided': roll_6}
            message = "{} rolled {} + {} = {}!".format(self.user_id, roll_4, roll_6, sum)
            result = sum
        elif type == "attack":
            ask_data = {'options': ['Roll for damage!']}
            display_data = {'type': 'roll', '4-sided': roll_4, '6-sided': roll_6}
            message = "{} rolled a {} - {} = {}!".format(self.user_id, max(roll_6, roll_4), min(roll_6, roll_4), diff)
            result = diff
        elif type == "6":
            ask_data = {'options': ['Roll the 6-sided die!']}
            display_data = {'type': 'roll', '4-sided': 0, '6-sided': roll_6}
            message = "{} rolled a {}!".format(self.user_id, roll_6)
            result = roll_6
        elif type == "4":
            ask_data = {'options': ['Roll the 4-sided die!']}
            display_data = {'type': 'roll', '4-sided': roll_4, '6-sided': 0}
            message = "{} rolled a {}!".format(self.user_id, roll_4)
            result = roll_4

        # Ask for confirmation and display results
        self.ask_h('confirm', ask_data, self.user_id)
        self.gc.show_h(display_data)
        self.gc.tell_h(message)
        return result

    def giveEquipment(self, receiver, eq):

        # Transfer equipment
        i = self.equipment.index(eq)
        eq = self.equipment.pop(i)
        receiver.equipment.append(eq)
        eq.holder = receiver

        # Tell frontend about transfer
        self.gc.tell_h("{} gave {} their {}!".format(self.user_id, receiver.user_id, eq.title))
        self.gc.update_h()

    def attack(self, other, amount, dryrun=False):

        # Compose equipment functions
        is_attack = True
        successful = (amount != 0)
        for eq in self.equipment:
            if eq.use:
                amount = eq.use(is_attack, successful, amount)

        # Check for spear of longinus
        has_spear = "Spear of Longinus" in [e.title for e in self.equipment]
        if successful and self.character.alleg == 2 and self.state == 1 and has_spear:
            if not dryrun:
                self.gc.tell_h("{} strikes with their Spear of Longinus!".format(self.user_id))
            amount += 2

        # Return damage dealt
        dealt = other.defend(self, amount, dryrun)

        # If we dealt damage, some specials might have external effects
        if dealt > 0:
            if 'damage_dealt_fn' in self.modifiers:
                self.modifiers['damage_dealt_fn'](self)

        return dealt

    def defend(self, other, amount, dryrun=False):

        # Check for guardian angel
        if "guardian_angel" in self.modifiers:
            if not dryrun:
                self.gc.tell_h("{}\'s Guardian Angel shielded them from damage!".format(self.user_id))
            return 0

        # Compose equipment functions
        is_attack = False
        successful = False
        for eq in self.equipment:
            if eq.use:
                amount = eq.use(is_attack, successful, amount)

        # Return damage dealt
        dealt = amount
        if not dryrun:
            self.moveDamage(-dealt, attacker = other)

        # Check for counterattack
        if self.modifiers['counterattack']:
            # Ask if player wants to counterattack
            answer = self.gc.ask_h('confirm', {'options': ["Counterattack", "Decline"]}, self.user_id)['value']

            if answer != "Decline":
                self.gc.tell_h("{} is counterattacking!".format(self.user_id))
                # Roll with the 4-sided die if the player has masamune
                roll_result = 0
                if "Cursed Sword Masamune" in [e.title for e in self.equipment]:
                    self.gc.tell_h("{} rolls with the 4-sided die using the Masamune!".format(self.user_id, roll_result))
                    roll_result = self.rollDice('4')
                else:
                    roll_result = self.rollDice(self.modifiers['attack_dice_type'])
                self.attack(other, roll_result)
            else:
                self.gc.tell_h("{} declined to counterattack.".format(self.user_id))

        return dealt

    def moveDamage(self, damage_change, attacker):
        if self.modifiers['steal_for_damage']:
            if damage_change >= 2:
                # Ask attacker whether to steal equipment or deal damage
                data = {'options': ["Steal equipment", "Deal {} damage".format(damage_change)]}
                choose_steal = (player.ask_h('select', data, player.user_id)['value'] == "Steal equipment")

                if choose_steal:
                    desired_eq = attacker.chooseEquipment(self)
                    self.giveEquipment(attacker, desired_eq)
                    gc.tell_h("{} stole {}'s {} instead of dealing {} damage!'".format(attacker.user_id, self.user_id, desired_eq.name, damage_change))

                    return self.damage

        self.damage = min(self.damage - damage_change, self.character.max_damage)
        self.damage = max(0, self.damage)
        self.checkDeath(attacker)
        return self.damage

    def setDamage(self, damage, attacker):
        self.damage = damage
        self.checkDeath(attacker)

    def checkDeath(self, attacker):
        if self.damage >= self.character.max_damage:
            self.die(attacker)
        self.gc.update_h()

    def die(self, attacker):
        # Set state to 0 (DEAD)
        self.state = 0

        # Report to console
        display_data = {'type': 'die', 'player': self.dump()}
        self.gc.show_h(display_data)
        self.gc.tell_h("{} ({}: {}) was killed by {}!".format(
            self.user_id,
            elements.ALLEGIANCE_MAP[self.character.alleg],
            self.character.name,
            attacker.user_id
        ))

        # Get dead player and their equipment
        data = {'options': [eq.title for eq in self.equipment]}
        if len(data['options']):

            has_silver_rosary = ("Silver Rosary" in [e.title for e in attacker.equipment])
            has_steal_all_mod = attacker.modifiers['steal_all_on_kill']

            if has_silver_rosary or has_steal_all_mod:

                # Steal all of the player's equipment
                msg = ""
                if has_silver_rosary:
                    msg = "{}'s Silver Rosary let them steal all of {}'s equipment!".format(attacker.user_id, self.user_id)
                else:
                    msg = "{} stole all of {}'s equipment!".format(attacker.user_id, self.user_id)

                self.gc.tell_h()
                attacker.equipment += self.equipment
                for eq in attacker.equipment:
                    eq.holder = attacker
                self.equipment = []
                self.gc.update_h()

            else:

                # Choose which equipment to take
                attacker.ask_h('confirm', {'options': ['Take equipment from {}'.format(self.user_id)]}, attacker.user_id)
                equip = attacker.ask_h('select', data, attacker.user_id)['value']
                equip_Equipment = [eq for eq in self.equipment if eq.title == equip][0]

                # Transfer equipment from one player to the other
                self.giveEquipment(attacker, equip_Equipment)

        # Put remaining equipment back in the deck (discard pile)
        while self.equipment:
            eq = self.equipment.pop()
            if eq.color == 1: # Black
                self.gc.black_cards.addToDiscard(eq)
            elif eq.color == 2: # Green
                self.gc.green_cards.addToDiscard(eq)
            elif eq.color == 3: # White
                self.gc.white_cards.addToDiscard(eq)

        # Set self to null location
        self.location = None

    def move(self, location):
        self.location = location
        self.gc.update_h()

    def dump(self):
        return {
            'user_id': self.user_id,
            'socket_id': self.socket_id,
            'state': self.state,
            'equipment': [eq.dump() for eq in self.equipment],
            'damage': self.damage,
            'character': self.character.dump() if self.character else {},
            'modifiers': self.modifiers,
            'location': self.location.dump() if self.location else {},
            'ai': self.ai,
        }
