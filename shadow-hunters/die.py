import random

# Die.py
# Implements a Die object with a specified number of sides.

class Die:
    def __init__(self, n_sides):

        # Make sure die has a positive number of sides
        if not n_sides > 0:
            raise ValueError("n_sides must be greater than 0")

        self.n_sides = n_sides
        self.state = None

    def roll(self):
        self.state = random.randint(1, self.n_sides)
        return self.state
