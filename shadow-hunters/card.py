# card.py
# Implements the Card object.


class Card:
    """
    A Card of any type.
    """

    def __init__(self, title, desc, type, holder, is_equip, use):
        self.title = title
        self.desc = desc
        self.type = type
        self.holder = holder
        self.is_equipment = is_equip
        self.use = use

    def dump(self):
        return {
            'title': self.title,
            'desc': self.desc,
            'color': self.type.name,
            'is_equip': self.is_equipment
        }
