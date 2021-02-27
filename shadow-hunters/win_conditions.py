import constants as C

# win_conditions.py


def shadow(gc, player):

    # Shadows win if all hunters are dead or 3 neutrals are dead
    def is_hunter(p): return p.character.alleg == C.Alleg.Hunter
    def is_neutral(p): return p.character.alleg == C.Alleg.Neutral

    h = [p for p in gc.getLivePlayers() if is_hunter(p)]
    n = [p for p in gc.getDeadPlayers() if is_neutral(p)]

    no_living_hunters = len(h) == 0
    neutrals_dead_3 = len(n) >= 3

    return no_living_hunters or neutrals_dead_3


def hunter(gc, player):

    # Hunters win if all shadows are dead
    def is_shadow(p): return p.character.alleg == C.Alleg.Shadow

    s = [p for p in gc.getLivePlayers() if is_shadow(p)]

    no_living_shadows = len(s) == 0

    return no_living_shadows


def allie(gc, player):

    # Allie wins if she is still alive when the game ends
    return (player in gc.getLivePlayers()) and gc.game_over


def bob(gc, player):

    # Bob wins if he has 5+ equipment cards
    return len(player.equipment) >= 5


def catherine(gc, player):

    # Catherine wins if she is the first to die or one of the last 2 remaining
    first_to_die = (player in gc.getDeadPlayers()) and (
        len(gc.getDeadPlayers()) == 1)
    last_two = (player in gc.getLivePlayers()) and (
        len(gc.getLivePlayers()) <= 2)
    return first_to_die or last_two


def charles(gc, player):
    return False
