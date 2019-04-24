# win_conditions.py

def shadow(gc, player):

    # Shadows win if all hunters are dead or 3 neutrals are dead
    no_living_hunters = (
        len([p for p in gc.getLivePlayers() if p.character.alleg == 2]) == 0)
    neutrals_dead_3 = (
        len([p for p in gc.getDeadPlayers() if p.character.alleg == 1]) >= 3)
    return no_living_hunters or neutrals_dead_3

def hunter(gc, player):

    # Hunters win if all shadows are dead
    no_living_shadows = (
        len([p for p in gc.getLivePlayers() if p.character.alleg == 0]) == 0)
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
