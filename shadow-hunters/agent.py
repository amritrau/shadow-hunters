import random


class AgentInterface():
    """Defines an agent that can interact with the game"""

    def __init__(self):
        pass

    def choose_action(self, options, player, gc):
        """Choose an action from the options provided"""

        raise NotImplementedError

    def choose_reveal(self, player, gc):
        """Return true if the agent chooses to reveal"""
        
        raise NotImplementedError


class RandomAgent(AgentInterface):
    """Defines an agent that randomly interacts with the game"""

    def choose_action(self, options, player, gc):
        """Randomly select an action from the options provided"""

        if 'Decline' in options and len(options) > 1:
            options.remove('Decline')
        return {'value': random.choice(options)}

    def choose_reveal(self, player, gc):
        """Randomly reveal identity with increasing probability as the
        game progresses"""

        reveal_chance = gc.round_count / 20
        return (random.random() <= reveal_chance)


Agent = RandomAgent
