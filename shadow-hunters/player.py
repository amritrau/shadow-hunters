class Player:
    def __init__(self, user_id):
        self.user_id = user_id
        self.game_context = None
        self.state = 2 #  2 for ALIVE_ANON, 1 for ALIVE_KNOWN, 0 for DEAD
        self.character = None
        self.equipment = []
        self.hp = None
        self.location = None
        self.modifiers = {}

    def setCharacter(self, character):
        self.character = character
        self.hp = self.character.max_hp

    def reveal(self):
        # self.character.special()
        self.status = 1

    def takeTurn(self):
        # 1. Roll dice
        # 2. Move to desired location
        # 3. Take action
        # 4. Attack

        raise NotImplementedError

    def drawCard(self, deck):
        drawn = deck.drawCard()
        if drawn.force_use:
            drawn.use()

    def attack(self, other):
        # TODO Help
        raise NotImplementedError

    def defend(self, other):
        # TODO Help
        raise NotImplementedError

    def move(self, location):
        # TODO Help
        self.location = location
        raise NotImplementedError


    # # The quick brown fox jumps over the lazy dog
