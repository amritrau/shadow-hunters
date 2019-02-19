# card.py
# Implements the Card object.

class Card:
    """
    A Card of any type.
    """
    def __init__(self, title, desc, color, holder, is_equip, force_use, use):
        self.title = title
        self.desc = desc
        self.color = color
        self.holder = holder
        self.is_equipment = is_equip
        self.force_use = force_use
        self.use = use

    def __str__(self):
        return "{}\n{}\n{}".format(self.title, '='*len(self.title), self.desc)
