import elements

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
        self.modifiers = {}
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
        self.gc.tell_h("{} revealed themselves as {}, a {} with {} hp!".format(
            self.user_id,
            self.character.name,
            elements.ALLEGIANCE_MAP[self.character.alleg],
            self.character.max_damage
        ))
        self.gc.tell_h("Their win condition: {}.".format(self.character.win_cond_desc))
        self.gc.tell_h("Their special ability: {}.".format("None"))

    def takeTurn(self):

        # Announce player
        self.gc.tell_h("It's {}'s turn!".format(self.user_id))

        # Guardian Angel wears off
        if "guardian_angel" in self.modifiers:
            self.gc.tell_h("The effect of {}\'s Guardian Angel wore off!".format(self.user_id))
            del self.modifiers["guardian_angel"]

        # Roll dice
        self.gc.tell_h("{} is rolling for movement...".format(self.user_id))
        data = {'options': ['Roll for movement!']}
        self.ask_h('confirm', data, self.user_id)
        roll_result_4 = self.gc.die4.roll()
        roll_result_6 = self.gc.die6.roll()
        roll_result = roll_result_4 + roll_result_6
        self.gc.tell_h("{} rolled {} + {} = {}!".format(self.user_id, roll_result_4, roll_result_6, roll_result))

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
        self.gc.tell_h("{} is picking whom to attack...".format(self.user_id))
        live_players = [p for p in self.gc.getLivePlayers() if p.location]
        targets = [p for p in live_players if (p.location.zone == self.location.zone and p != self)]
        data = {'options': [t.user_id for t in targets] + ['Decline']}
        answer = self.ask_h('select', data, self.user_id)['value']

        if answer != 'Decline':

            # Get target and ask for roll
            target_name = answer
            target_Player = [p for p in self.gc.getLivePlayers() if p.user_id == target_name][0]
            self.gc.tell_h("{} is attacking {}!".format(self.user_id, target_name))
            data = {'options': ['Roll for damage!']}
            self.ask_h('confirm', data, self.user_id)

            # Get attack roll
            roll_result_4 = self.gc.die4.roll()
            roll_result_6 = self.gc.die6.roll()
            roll_result = abs(roll_result_4 - roll_result_6)
            self.gc.tell_h(
                "{} rolled a {} - {} = {}!".format(
                    self.user_id,
                    max(roll_result_6, roll_result_4),
                    min(roll_result_6, roll_result_4),
                    roll_result
                )
            )

            # Get damage dealt
            damage_dealt = self.attack(target_Player, roll_result)
            self.gc.tell_h("{} hit {} for {} damage!".format(self.user_id, target_name, damage_dealt))
        else:
            self.gc.tell_h("{} declined to attack.".format(self.user_id))

        # The current player could have died -- if so end their turn
        if self.state == 0:
            return

        # Turn is over
        self.gc.tell_h("{}'s turn is over.".format(self.user_id))

    def drawCard(self, deck):

        # Draw card and tell people about it
        drawn = deck.drawCard()
        public_title = drawn.title if drawn.color != 2 else 'a Hermit Card'
        self.gc.tell_h("{} drew {}!".format(self.user_id, public_title))
        if drawn.color != 2:
            self.gc.tell_h("{}: {}".format(drawn.title, drawn.desc))
        else:
            self.gc.direct_h("{}: {}".format(drawn.title, drawn.desc), self.socket_id)

        # Use card if it's single-use, or add to arsenal if it's equipment
        if drawn.is_equipment:
            self.gc.tell_h("{} added {} to their arsenal!".format(self.user_id, public_title))
            self.equipment.append(drawn)
            self.gc.update_h()
        else:
            args = {'self': self, 'card': drawn}
            drawn.use(args)

    def attack(self, other, amount):

        # Compose equipment functions
        is_attack = True
        successful = (amount != 0)
        for eq in self.equipment:
            amount = eq.use(is_attack, successful, amount)

        # Return damage dealt
        dealt = other.defend(self, amount)
        return dealt

    def defend(self, other, amount):

        # Check for guardian angel
        if "guardian_angel" in self.modifiers:
            self.gc.tell_h("{}\'s Guardian Angel shielded them from damage!".format(self.user_id))
            return 0

        # Compose equipment functions
        is_attack = False
        successful = False
        for eq in self.equipment:
            amount = eq.use(is_attack, successful, amount)

        # Return damage dealt
        dealt = amount
        self.moveDamage(-dealt, attacker = other)
        return dealt

    def moveDamage(self, damage_change, attacker):
        self.damage = min(self.damage - damage_change, self.character.max_damage)
        self.damage = max(0, self.damage)
        self.checkDeath(attacker)
        return self.damage

    def setDamage(self, damage, attacker):
        self.damage = damage
        self.checkDeath(attacker)

    def checkDeath(self, attacker):
        if self.damage >= self.character.max_damage:
            self.state = 0
            self.gc.tell_h("{} ({}: {}) was killed by {}!".format(
                self.user_id,
                elements.ALLEGIANCE_MAP[self.character.alleg],
                self.character.name,
                attacker.user_id
            ))
        self.gc.update_h()

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
