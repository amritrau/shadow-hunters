import elements

# card.py
# Implements the Card object.


class Card:
    """
    A Card of any type.
    """

    def __init__(self, title, desc, color, holder, is_equip, use):
        self.title = title
        self.desc = desc
        self.color = color
        self.holder = holder
        self.is_equipment = is_equip
        self.use = use

    def dump(self):
        return {
            'title': self.title,
            'desc': self.desc,
            'color': elements.CARD_COLOR_MAP[self.color],
            'is_equip': self.is_equipment
        }
