import cli

class Player:
    def __init__(self, user_id, socket_id):
        self.user_id = user_id
        self.socket_id = socket_id
        self.gc = None # game context (abbreviated for convenience)
        self.state = 2 #  2 for ALIVE_ANON, 1 for ALIVE_KNOWN, 0 for DEAD
        self.character = None
        self.equipment = []
        self.hp = 0
        self.location = None
        self.modifiers = {}

    def setCharacter(self, character):
        self.character = character

    def reveal(self):
        # self.character.special()
        self.state = 1

    def takeTurn(self):
        # Announce player
        self.gc.tell_h("It's {}'s turn!".format(self.user_id))

        # Roll dice
        self.gc.tell_h("{} is rolling for movement...".format(self.user_id))
        data = {'options': ['Roll for movement!']}
        self.gc.ask_h('confirm', data, self.user_id)

        roll_result_4 = self.gc.die4.roll()
        roll_result_6 = self.gc.die6.roll()
        roll_result = roll_result_4 + roll_result_6

        self.gc.tell_h("{} rolled {} + {} = {}!".format(self.user_id, roll_result_4, roll_result_6, roll_result))
        self.gc.update_h()

        # Move to desired location
        if roll_result == 7:
            # Select an area
            self.gc.tell_h("{} is selecting an area...".format(self.user_id))
            area_options = []
            for z in self.gc.zones:  # TODO again, shameful
                for a in z.areas:
                    area_options.append(a.name)
            data = {
                'options': area_options
            }
            destination = self.gc.ask_h('select', data, self.user_id)['value']

            # Get Area object from area name
            destination_Area = None
            for z in self.gc.zones:
                for a in z.areas:
                    if a.name == destination:
                        destination_Area = a

        else:
            # Get Area from roll
            destination_Area = None # TODO this is shameful
            for z in self.gc.zones:
                for a in z.areas:
                    if roll_result in a.domain:
                        destination_Area = a

            # Get string from Area
            destination = destination_Area.name

        self.move(destination_Area)
        self.gc.update_h()
        self.gc.tell_h("{} moves to {}!".format(self.user_id, destination))


        # Take action
        data = {'options': [destination_Area.desc, 'Decline']}

        answer = self.gc.ask_h('yesno', data, self.user_id)['value']
        if answer != 'Decline':
            # TODO Update game state
            # self.gc.update_h()

            # TODO Perform area action
            self.location.action(self.gc, self)
            self.gc.tell_h(
                '{} performed their area action!'.format(self.user_id)
            )
            self.gc.update_h()
        else:
            self.gc.tell_h(
                '{} declined to perform their area action.'.format(self.user_id)
            )
            self.gc.update_h()

        # Someone could have died here, so check win conditions
        if self.gc.checkWinConditions(tell = False):
            return  # let the win conditions check in GameContext.play() handle

        # Attack
        self.gc.tell_h("{} is picking whom to attack...".format(self.user_id))
        live_players = [p for p in self.gc.getLivePlayers() if p.location]
        targets = [
            p for p in live_players if (p.location.zone == self.location.zone and p != self)
        ]
        data = {'options': [t.user_id for t in targets] + ['Decline']}
        answer = self.gc.ask_h('select', data, self.user_id)['value']
        self.gc.update_h()

        if answer != 'Decline':
            target = answer
            target_Player = [p for p in self.gc.getLivePlayers() if p.user_id == target]  # TODO Amrit do you even know Python
            target_Player = target_Player[0]
            self.gc.tell_h("{} is attacking {}!".format(self.user_id, target))
            data = {'options': ['Roll for damage!']}
            self.gc.ask_h('confirm', data, self.user_id)

            roll_result_4 = self.gc.die4.roll()
            roll_result_6 = self.gc.die6.roll()
            roll_result = abs(roll_result_4 - roll_result_6)
            self.gc.update_h(),
                        min(roll_result_6, roll_result_4)
                    )
                }
            )
            self.gc.tell_h(
                "{} rolled a {} - {} = {}!".format(
                    self.user_id,
                    max(roll_result_6, roll_result_4),
                    min(roll_result_6, roll_result_4),
                    roll_result
                )
            )

            damage_dealt = self.attack(target_Player, roll_result)

            self.gc.update_h()
            self.gc.tell_h(
                "{} hit {} for {} damage!".format(
                    self.user_id, target, damage_dealt
                )
            )
        else:
            self.gc.tell_h("{} declined to attack.".format(self.user_id))

        # Turn is over
        self.gc.tell_h("{}'s turn is over.".format(self.user_id))

    def drawCard(self, deck):
        drawn = deck.drawCard()
        public_title = drawn.title if drawn.color != 2 else 'a Hermit Card'
        self.gc.tell_h("{} drew {}!".format(self.user_id, public_title))
        self.gc.direct_h("Card ({}): {}".format(drawn.title, drawn.desc), self.socket_id)
        if drawn.force_use:
            self.gc.tell_h("{} used {}!".format(self.user_id, public_title))
            args = {'self': self}
            drawn.use(args)
        if drawn.is_equipment:
            self.gc.tell_h("{} added {} to their arsenal!".format(self.user_id, public_title))
            self.equipment.append(drawn)
        self.gc.update_h()

    def attack(self, other, amount):
        is_attack = True
        successful = (amount != 0)
        for eq in self.equipment:
            amount = eq.use(is_attack, successful, amount) # Compose each of these functions

        dealt = other.defend(self, amount)
        return dealt

    def defend(self, other, amount):
        is_attack = False
        successful = False # irrelevant for defend
        for eq in self.equipment:
            amount = eq.use(is_attack, successful, amount) # Compose each of these functions

        dealt = amount
        self.moveHP(-dealt)
        return dealt

    def moveHP(self, hp_change):
        self.hp = min(self.hp - hp_change, self.character.max_hp)
        self.hp = max(0, self.hp)
        self.checkDeath()
        return self.hp

    def setHP(self, hp):
        self.hp = hp
        self.checkDeath()

    def checkDeath(self):
        if self.hp >= self.character.max_hp:
            self.state = 0  # DEAD state
            self.gc.tell_h("{} ({}: {}) died!".format(self.user_id, cli.ALLEGIANCE_MAP[self.character.alleg], self.character.name))
        else: ## TODO Remove when not debugging
            self.gc.tell_h("{}'s HP was set to {}!".format(self.user_id, self.hp))

        self.gc.update_h()

    def move(self, location):
        # TODO What checks do we need here?
        self.location = location
        self.gc.update_h()

    def dump(self):
        return {
            'user_id': self.user_id,
            'socket_id': self.socket_id,
            'state': self.state,
            'equipment': [eq.dump() for eq in self.equipment],
            'hp': self.hp,
            'character': self.character.dump() if self.character else {},
            'modifiers': self.modifiers,
            'location': self.location.dump() if self.location else {},
        }
