import random


class Agent:
    """Defines an agent that's capable of interacting with the game"""
    def __init__(self):
        pass

    def choose_action(self, options, sleep=0, gc=None):
        """Choose an action from the options provided"""
        socketio.sleep(sleep)
        if 'Decline' in options and len(options) > 1:
            options.remove('Decline')
        return {'value': random.choice(options)}

    def choose_reveal(self, gc):
        """Return true if the agent chooses to reveal"""
        reveal_chance = gc.round_count / 20
        return (random.random() <= reveal_chance)
