# character.py
# Implements a Character.

class Character:
    def __init__(self, name, alleg, max_hp, win_cond, win_cond_desc, resource_id, special):
        self.name = name
        self.alleg = alleg
        self.max_hp = max_hp
        self.win_cond = win_cond
        self.win_cond_desc = win_cond_desc
        self.special = special
        self.resource_id = resource_id

    def dump(self):
        return {
            'name': self.name,
            'alleg': self.alleg,
            'max_hp': self.max_hp,
            'win_cond_desc': self.win_cond_desc,
            'resource_id': self.resource_id
        }
