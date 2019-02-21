import random

# Die.py
# Implements a Die object with a specified number of sides.

class Die:
    def __init__(self, n_sides):
        self.n_sides = n_sides
        self.state = None

    def roll(self):
        self.state = random.randint(1, n_sides)
        return self.state
