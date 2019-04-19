# character.py
# Implements a Character.

class Character:
    def __init__(self, name, alleg, max_damage, win_cond, win_cond_desc, resource_id, special, special_desc, modifiers = {'min_players': 4, 'max_players': 8}):
        self.name = name
        self.alleg = alleg
        self.max_damage = max_damage
        self.win_cond = win_cond
        self.win_cond_desc = win_cond_desc
        self.special = special
        self.special_desc = special_desc
        self.resource_id = resource_id
        self.modifiers = modifiers

    def dump(self):
        return {
            'name': self.name,
            'alleg': self.alleg,
            'max_damage': self.max_damage,
            'win_cond_desc': self.win_cond_desc,
            'special_desc': self.special_desc,
            'resource_id': self.resource_id
        }
