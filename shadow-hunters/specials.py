# specials.py

# Neutrals


def allie(gc, player, turn_pos):
    # ANY TIME
    if turn_pos == 'now':
        if not player.modifiers['special_used']:

            # Tell
            gc.tell_h("{} ({}) used their special ability: {}", [
                      player.user_id, player.character.name, player.character.special_desc])

            # Full heal
            player.setDamage(0, player)

            # Update modifiers
            player.modifiers['special_used'] = True


def bob(gc, player, turn_pos):
    if not player.modifiers['special_used']:
        if 4 <= len(gc.players) <= 6:
            player.modifiers['steal_for_damage'] = True
        else:
            # Update modifiers
            player.modifiers['steal_all_on_kill'] = True


def catherine(gc, player, turn_pos):
    # START OF TURN
    if turn_pos == 'start' and (not player.modifiers['special_used']):

        # Tell
        gc.tell_h("{} ({}) used their special ability: {}", [
                  player.user_id, player.character.name, player.character.special_desc])

        # Catherine is *required* to heal at the beginning of the turn
        player.moveDamage(1, player)

# Hunters


def george(gc, player, turn_pos):
    # START OF TURN
    if turn_pos == 'start':
        if not player.modifiers['special_used']:
            player.modifiers['special_used'] = True

            # Tell
            gc.tell_h("{} ({}) used their special ability: {}", [
                      player.user_id, player.character.name, player.character.special_desc])

            # Present player with list of attack options
            targets = [p for p in gc.getLivePlayers()]
            gc.tell_h("{} is choosing a target...", [player.user_id])
            target_Player = player.choosePlayer()
            gc.tell_h("{} chose {}!", [
                      player.user_id, target_Player.user_id])

            # Roll and give damage to target
            roll_result = player.rollDice('4')
            target_Player.moveDamage(-1 * roll_result, player)
            gc.tell_h("{}'s Hammer gave {} {} damage!", [
                      player.user_id, target_Player.user_id, roll_result])


def fuka(gc, player, turn_pos):
    # START OF TURN
    if turn_pos == 'start':
        if not player.modifiers['special_used']:
            player.modifiers['special_used'] = True

            # Tell
            gc.tell_h("{} ({}) used their special ability: {}", [
                      player.user_id, player.character.name, player.character.special_desc])

            # Enter set damage to 7 sequence
            # Select a player to use special on (includes user)
            player.gc.ask_h(
                'confirm', {'options': ["Use special ability"]}, player.user_id)
            data = {'options': [
                t.user_id for t in gc.getLivePlayers()]}
            target = player.gc.ask_h(
                'select', data, player.user_id)['value']

            # Set selected player to 7 damage
            target_Player = [
                p for p in gc.getLivePlayers() if p.user_id == target][0]
            target_Player.setDamage(7, player)
            gc.tell_h("{} gave a killing cure to {}!", [
                      player.user_id, target_Player.user_id])


def franklin(gc, player, turn_pos):

    if turn_pos == 'start':
        if not player.modifiers['special_used']:
            player.modifiers['special_used'] = True

            # Tell
            gc.tell_h("{} ({}) used their special ability: {}", [
                      player.user_id, player.character.name, player.character.special_desc])

            # Present player with list of attack options
            gc.tell_h("{} is choosing a target...", [player.user_id])
            target_Player = player.choosePlayer()
            gc.tell_h("{} chose {}!", [
                      player.user_id, target_Player.user_id])

            # Roll and give damage to target
            roll_result = player.rollDice('6')
            target_Player.moveDamage(-1 * roll_result, player)
            gc.tell_h("{}'s Lightning gave {} {} damage!", [
                      player.user_id, target_Player.user_id, roll_result])


def ellen(gc, player, turn_pos):
    # START OF TURN
    if turn_pos == 'start':
        if not player.modifiers['special_used']:
            player.modifiers['special_used'] = True

            # Tell
            gc.tell_h("{} ({}) used their special ability: {}", [
                      player.user_id, player.character.name, player.character.special_desc])

            # Choose a player to cancel their special
            target_Player = player.choosePlayer()

            # Cancel special
            target_Player.resetModifiers()
            target_Player.modifiers['special_used'] = True
            target_Player.special = lambda gc, player, turn_pos: gc.tell_h(
                "Your special ability was voided by {}.", [player.user_id], player.socket_id)
            gc.tell_h("{} voided {}'s special ability for the rest of the game!", [
                      player.user_id, target_Player.user_id])

# Shadows


def valkyrie(gc, player, turn_pos):
    if (not player.modifiers['special_active']) and (
            not player.modifiers['special_used']):
        # Tell
        gc.tell_h("{} ({}) used their special ability: {}", [
                  player.user_id, player.character.name, player.character.special_desc])
        player.modifiers['attack_dice_type'] = "4"
        player.modifiers['special_active'] = True


def vampire(gc, player, turn_pos):
    if (not player.modifiers['special_active']) and (
            not player.modifiers['special_used']):
        # Tell
        gc.tell_h("{} ({}) used their special ability: {}", [
                  player.user_id, player.character.name, player.character.special_desc])
        player.modifiers['damage_dealt_fn'] = lambda player: player.moveDamage(
            2, player)
        player.modifiers['special_active'] = True


def werewolf(gc, player, turn_pos):
    if not player.modifiers['special_used']:
        player.modifiers['counterattack'] = True
        player.modifiers['special_active'] = True


def ultra_soul(gc, player, turn_pos):
    # START OF TURN
    if turn_pos == 'start' and (not player.modifiers['special_used']):
        # No need to bother every turn if there's nobody at UG
        targets = gc.getPlayersAt("Underworld Gate")
        targets = [t for t in targets if t != player]
        if len(targets) > 0:
            # Present player with list of attack options
            gc.tell_h("{} ({}) used their special ability: {}", [
                      player.user_id, player.character.name, player.character.special_desc])
            gc.tell_h("{} is choosing a target...", [player.user_id])
            data = {'options': [
                p.user_id for p in targets if p != player]}
            target = player.gc.ask_h(
                'select', data, player.user_id)['value']
            target_Player = [
                p for p in gc.getLivePlayers() if p.user_id == target][0]
            target_Player.moveDamage(-3, player)
            gc.tell_h("{}'s Murder Ray gave {} {} damage!",
                      [player.user_id, target, 3])
