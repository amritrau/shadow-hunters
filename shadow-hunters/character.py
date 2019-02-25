# character.py
# Implements a Character.

class Character:
    def __init__(self, name, alleg, max_hp, win_cond, resource_id, special):
        self.name = name
        self.alleg = alleg
        self.max_hp = max_hp
        self.win_cond = win_cond
        self.special = special
        self.resource_id = resource_id
