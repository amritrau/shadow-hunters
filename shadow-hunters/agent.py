import random
import json


class Agent:
    """Defines an agent that's capable of interacting with the game"""
    def __init__(self):
        pass

    def choose_action(self, options, player, gc):
        """Choose an action from the options provided"""

        # public_state, private_state = gc.dump()
        # priv = [p for p in private_state if p['user_id'] == ]
        # print(json.dumps(public_state['players'], indent=4))
        # print(json.dumps(private_state, indent=4))

        if 'Decline' in options and len(options) > 1:
            options.remove('Decline')
        return {'value': random.choice(options)}

    def choose_reveal(self, player, gc):
        """Return true if the agent chooses to reveal"""
        reveal_chance = gc.round_count / 20
        return (random.random() <= reveal_chance)
