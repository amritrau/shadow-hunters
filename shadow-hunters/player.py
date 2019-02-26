class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.gc = None # game context (abbreviated for convenience)
        self.state = 2 #  2 for ALIVE_ANON, 1 for ALIVE_KNOWN, 0 for DEAD
        self.character = None
        self.equipment = []
        self.hp = None
        self.location = None
        self.modifiers = {}

    def setCharacter(self, character):
        self.character = character
        self.win_cond = win_cond
        self.hp = self.character.max_hp

    def reveal(self):
        # self.character.special()
        self.status = 1

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

        self.gc.update_h('confirm', {'action': 'roll', 'value': (roll_result_4, roll_result_6)})
        self.gc.tell_h("{} rolled {} + {} = {}!".format(self.user_id, roll_result_4, roll_result_6, roll_result))

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
            # TODO Will not work until #12 is resolved
            destination = self.gc.ask_h('select', data, self.user_id)['value']

            # Get Area object from area name
            # destination_Area = [a for a in z.areas for z in self.gc.zones if a.name == destination][0]  # TODO fix this garbage
            destination_Area = None
            for z in self.gc.zone:
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
            # destination_Area = [(a for a in z.areas for z in self.gc.zones if roll_result in a.domain][0]

            # Get string from Area
            destination = destination_Area.name

        self.gc.update_h('select', {'action': 'move', 'value': destination})
        self.gc.tell_h("{} moves to {}!".format(self.user_id, destination))
        self.move(destination_Area)

        # Take action
        data = {'options': ['Perform area action', 'Decline']}
        # TODO Won't work until #12 fixed
        answer = self.gc.ask_h('yesno', data, self.user_id)['value']
        if answer != 'Decline':
            # TODO Perform area action
            # TODO Update game state
            self.gc.update_h('yesno', {'action': 'area', 'value': 'TODO'})
            self.gc.tell_h(
                '{} performed their area action!'.format(self.user_id)
            )
        else:
            self.gc.update_h('yesno', {})
            self.gc.tell_h(
                '{} declined to perform their area action.'.format(self.user_id)
            )

        # Attack
        self.gc.tell_h("{} is picking whom to attack...".format(self.user_id))
        live_players = [p for p in self.gc.players if p.location]
        targets = [
            p for p in live_players if (p.location.zone == self.location.zone and p != self)
        ]
        data = {'options': [t.user_id for t in targets] + ['Decline']}

        # TODO This fails until issue #12 is fixed
        answer = self.gc.ask_h('select', data, self.user_id)['value']
        # End failure

        self.gc.update_h('select', {})

        if answer != 'Decline':
            target = answer
            target_Player = [p for p in self.gc.players if p.user_id == target]  # TODO Amrit do you even know Python
            target_Player = target_Player[0]
            self.gc.tell_h("{} is attacking {}!".format(self.user_id, target))
            data = {'options': ['Roll for damage!']}
            self.gc.ask_h('confirm', data, self.user_id)

            roll_result_4 = self.gc.die4.roll()
            roll_result_6 = self.gc.die6.roll()
            roll_result = abs(roll_result_4 - roll_result_6)
            self.gc.update_h(
                'confirm',
                {
                    'action': 'roll',
                    'value': (
                        max(roll_result_6, roll_result_4),
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

            self.gc.update_h(
                'none', {
                    'action': 'damage',
                    'player': target,
                    'value': damage_dealt
                }
            )
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
        if drawn.force_use:
            drawn.use()
        if drawn.is_equipment:
            self.equipment.append(drawn)

    def attack(self, other, amount):
        for eq in self.equipment:
            amount = eq.use(True, amount) # Compose each of these functions
            # "True" argument refers to is_attack

        dealt = other.defend(self, amount)
        return dealt

    def defend(self, other, amount):
        for eq in self.equipment:
            amount = eq.use(False, amount) # Compose each of these functions
            # "False" argument refers to is_attack
        dealt = amount
        self.hp -= dealt
        return dealt

    def move(self, location):
        # TODO What checks do we need here?
        self.location = location
