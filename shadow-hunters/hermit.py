import constants

# hermit.py

def blackmail(args):

    # Choose a player to give the card to
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Hermit's Blackmail"]}, args['self'].user_id)
    target = args['self'].choosePlayer()
    display_data = args['card'].dump()
    display_data['type'] = 'draw'
    args['self'].gc.show_h(display_data, target.socket_id)

    # If target is neutral or hunter, must give equipment or take 1 damage
    if target.character.alleg > 0:

        # Target is neutral or hunter, get decision
        target.gc.tell_h("You are a {}.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        if len(target.equipment):
            data = {'options': [
                "Give an equipment card", "Receive 1 damage"]}
        else:
            data = {'options': ["Receive 1 damage"]}
        decision = target.gc.ask_h(
            'yesno', data, target.user_id)['value']

        # Branch on decision
        if decision == "Give an equipment card":

            # Target chooses an equipment card to give away
            eq = target.chooseEquipment(target)

            # Transfer equipment from target to user
            target.giveEquipment(args['self'], eq)

        else:

            # Target takes 1 damage
            new_damage = target.moveDamage(-1, args['self'])
            target.gc.tell_h("{} took {} damage!",
                             [target.user_id, "1"])

    else:

        # Target is a shadow, nothing happens
        target.gc.tell_h("You are a {}. Do nothing.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        data = {'options': ['Do nothing']}
        target.gc.ask_h('confirm', data, target.user_id)
        target.gc.tell_h("{} did nothing.", [target.user_id])

def greed(args):

    # Choose a player to give the card to
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Hermit's Greed"]}, args['self'].user_id)
    target = args['self'].choosePlayer()
    display_data = args['card'].dump()
    display_data['type'] = 'draw'
    args['self'].gc.show_h(display_data, target.socket_id)

    # If target is neutral or shadow, must give equipment or take 1 damage
    if target.character.alleg < 2:

        # Target is neutral or shadow, get decision
        target.gc.tell_h("You are a {}.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        if len(target.equipment):
            data = {'options': [
                "Give an equipment card", "Receive 1 damage"]}
        else:
            data = {'options': ["Receive 1 damage"]}
        decision = target.gc.ask_h(
            'yesno', data, target.user_id)['value']

        # Branch on decision
        if decision == "Give an equipment card":

            # Target chooses an equipment card to give away
            eq = target.chooseEquipment(target)

            # Transfer equipment from target to user
            target.giveEquipment(args['self'], eq)

        else:

            # Target takes 1 damage
            new_damage = target.moveDamage(-1, args['self'])
            target.gc.tell_h("{} took {} damage!",
                             [target.user_id, "1"])

    else:

        # Target is a hunter, nothing happens
        target.gc.tell_h("You are a {}. Do nothing.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        data = {'options': ['Do nothing']}
        target.gc.ask_h('confirm', data, target.user_id)
        target.gc.tell_h("{} did nothing.", [target.user_id])

def anger(args):

    # Choose a player to give the card to
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Hermit's Anger"]}, args['self'].user_id)
    target = args['self'].choosePlayer()
    display_data = args['card'].dump()
    display_data['type'] = 'draw'
    args['self'].gc.show_h(display_data, target.socket_id)

    # If target is hunter or shadow, must give equipment or take 1 damage
    if target.character.alleg in [0, 2]:

        # Target is hunter or shadow, get decision
        target.gc.tell_h("You are a {}.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        if len(target.equipment):
            data = {'options': [
                "Give an equipment card", "Receive 1 damage"]}
        else:
            data = {'options': ["Receive 1 damage"]}
        decision = target.gc.ask_h(
            'yesno', data, target.user_id)['value']

        # Branch on decision
        if decision == "Give an equipment card":

            # Target chooses an equipment card to give away
            eq = target.chooseEquipment(target)

            # Transfer equipment from target to user
            target.giveEquipment(args['self'], eq)

        else:

            # Target takes 1 damage
            new_damage = target.moveDamage(-1, args['self'])
            target.gc.tell_h("{} took {} damage!",
                             [target.user_id, "1"])

    else:

        # Target is a neutral, nothing happens
        target.gc.tell_h("You are a {}. Do nothing.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        data = {'options': ['Do nothing']}
        target.gc.ask_h('confirm', data, target.user_id)
        target.gc.tell_h("{} did nothing.", [target.user_id])

def slap(args):

    # Choose a player to give the card to
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Hermit's Slap"]}, args['self'].user_id)
    target = args['self'].choosePlayer()
    display_data = args['card'].dump()
    display_data['type'] = 'draw'
    args['self'].gc.show_h(display_data, target.socket_id)

    # If hunter, take 1 damage
    if target.character.alleg == 2:

        # Prompt target to receive 1 damage
        target.gc.tell_h("You are a {}.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        data = {'options': ["Receive 1 damage"]}
        target.gc.ask_h('confirm', data, target.user_id)

        # Give 1 damage to target
        new_damage = target.moveDamage(-1, args['self'])
        target.gc.tell_h("{} took {} damage!", [target.user_id, "1"])

    else:

        # Target is not a hunter, nothing happens
        target.gc.tell_h("You are a {}. Do nothing.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        data = {'options': ['Do nothing']}
        target.gc.ask_h('confirm', data, target.user_id)
        target.gc.tell_h("{} did nothing.", [target.user_id])

def spell(args):

    # Choose a player to give the card to
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Hermit's Spell"]}, args['self'].user_id)
    target = args['self'].choosePlayer()
    display_data = args['card'].dump()
    display_data['type'] = 'draw'
    args['self'].gc.show_h(display_data, target.socket_id)

    # If shadow, take 1 damage
    if target.character.alleg == 0:

        # Prompt target to receive 1 damage
        target.gc.tell_h("You are a {}.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        data = {'options': ["Receive 1 damage"]}
        target.gc.ask_h('confirm', data, target.user_id)

        # Give 1 damage to target
        new_damage = target.moveDamage(-1, args['self'])
        target.gc.tell_h("{} took {} damage!", [target.user_id, "1"])

    else:

        # Target is not a shadow, nothing happens
        target.gc.tell_h("You are a {}. Do nothing.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        data = {'options': ['Do nothing']}
        target.gc.ask_h('confirm', data, target.user_id)
        target.gc.tell_h("{} did nothing.", [target.user_id])

def exorcism(args):

    # Choose a player to give the card to
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Hermit's Exorcism"]}, args['self'].user_id)
    target = args['self'].choosePlayer()
    display_data = args['card'].dump()
    display_data['type'] = 'draw'
    args['self'].gc.show_h(display_data, target.socket_id)

    # If shadow, take 2 damage
    if target.character.alleg == 0:
        # Prompt target to receive 2 damage
        target.gc.tell_h("You are a {}.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        data = {'options': ["Receive 2 damage"]}
        target.gc.ask_h('confirm', data, target.user_id)

        # Give 2 damage to target
        new_damage = target.moveDamage(-2, args['self'])
        target.gc.tell_h("{} took {} damage!", [target.user_id, "2"])

    else:

        # Target is not a shadow, nothing happens
        target.gc.tell_h("You are a {}. Do nothing.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        data = {'options': ['Do nothing']}
        target.gc.ask_h('confirm', data, target.user_id)
        target.gc.tell_h("{} did nothing.", [target.user_id])

def nurturance(args):

    # Choose a player to give the card to
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Hermit's Nurturance"]}, args['self'].user_id)
    target = args['self'].choosePlayer()
    display_data = args['card'].dump()
    display_data['type'] = 'draw'
    args['self'].gc.show_h(display_data, target.socket_id)

    # If neutral, heal 1 damage (unless at 0, then take 1 damage)
    if target.character.alleg == 1:
        # Branch on hp value
        target.gc.tell_h("You are a {}.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        if target.damage == 0:

            # Hp is 0, prompt to receive 1 damage
            data = {'options': ["Receive 1 damage"]}
            target.gc.ask_h('confirm', data, target.user_id)

            # Give target 1 damage
            new_damage = target.moveDamage(-1, args['self'])
            target.gc.tell_h("{} took {} damage!",
                             [target.user_id, "2"])

        else:

            # Hp is nonzero, prompt to heal 1 damage
            data = {'options': ["Heal 1 damage"]}
            target.gc.ask_h('confirm', data, target.user_id)

            # Heal target 1 damage
            new_damage = target.moveDamage(1, args['self'])
            target.gc.tell_h("{} healed {} damage!",
                             [target.user_id, "1"])

    else:

        # Target is not a neutral, nothing happens
        target.gc.tell_h("You are a {}. Do nothing.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        data = {'options': ['Do nothing']}
        target.gc.ask_h('confirm', data, target.user_id)
        target.gc.tell_h("{} did nothing.", [target.user_id])

def aid(args):

    # Choose a player to give the card to
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Hermit's Aid"]}, args['self'].user_id)
    target = args['self'].choosePlayer()
    display_data = args['card'].dump()
    display_data['type'] = 'draw'
    args['self'].gc.show_h(display_data, target.socket_id)

    # If hunter, heal 1 damage (unless at 0, then take 1 damage)
    if target.character.alleg == 2:
        # Branch on hp value
        target.gc.tell_h("You are a {}.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        if target.damage == 0:

            # Hp is 0, prompt to receive 1 damage
            data = {'options': ["Receive 1 damage"]}
            target.gc.ask_h('confirm', data, target.user_id)

            # Give target 1 damage
            new_damage = target.moveDamage(-1, args['self'])
            target.gc.tell_h("{} took {} damage!",
                             [target.user_id, "1"])

        else:

            # Hp is nonzero, prompt to heal 1 damage
            data = {'options': ["Heal 1 damage"]}
            target.gc.ask_h('confirm', data, target.user_id)

            # Heal target 1 damage
            new_damage = target.moveDamage(1, args['self'])
            target.gc.tell_h("{} healed {} damage!",
                             [target.user_id, "1"])

    else:

        # Target is not a hunter, nothing happens
        target.gc.tell_h("You are a {}. Do nothing.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        data = {'options': ['Do nothing']}
        target.gc.ask_h('confirm', data, target.user_id)
        target.gc.tell_h("{} did nothing.", [target.user_id])

def huddle(args):

    # Choose a player to give the card to
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Hermit's Huddle"]}, args['self'].user_id)
    target = args['self'].choosePlayer()
    display_data = args['card'].dump()
    display_data['type'] = 'draw'
    args['self'].gc.show_h(display_data, target.socket_id)

    # If shadow, heal 1 damage (unless at 0, then take 1 damage)
    if target.character.alleg == 0:
        # Branch on hp value
        target.gc.tell_h("You are a {}.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        if target.damage == 0:

            # Hp is 0, prompt to receive 1 damage
            data = {'options': ["Receive 1 damage"]}
            target.gc.ask_h('confirm', data, target.user_id)

            # Give target 1 damage
            new_damage = target.moveDamage(-1, args['self'])
            target.gc.tell_h("{} took {} damage!",
                             [target.user_id, "1"])

        else:

            # Hp is nonzero, prompt to heal 1 damage
            data = {'options': ["Heal 1 damage"]}
            target.gc.ask_h('confirm', data, target.user_id)

            # Heal target 1 damage
            new_damage = target.moveDamage(1, args['self'])
            target.gc.tell_h("{} healed {} damage!",
                             [target.user_id, "1"])

    else:

        # Target is not a shadow, nothing happens
        target.gc.tell_h("You are a {}. Do nothing.", [
                         constants.ALLEGIANCE_MAP[target.character.alleg]], target.socket_id)
        data = {'options': ['Do nothing']}
        target.gc.ask_h('confirm', data, target.user_id)
        target.gc.tell_h("{} did nothing.", [target.user_id])

def lesson(args):

    # Choose a player to give the card to
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Hermit's Lesson"]}, args['self'].user_id)
    target = args['self'].choosePlayer()
    display_data = args['card'].dump()
    display_data['type'] = 'draw'
    args['self'].gc.show_h(display_data, target.socket_id)

    # If target's hp is >= 12, they take 2 damage.
    if target.character.max_damage >= 12:

        # Prompt target to receive 2 damage
        target.gc.tell_h("Your maximum hp ({}) is {} or more.", [
                         target.character.max_damage, "12"], target.socket_id)
        data = {'options': ["Receive 2 damage"]}
        target.gc.ask_h('confirm', data, target.user_id)

        # Give 2 damage to target
        new_damage = target.moveDamage(-2, args['self'])
        target.gc.tell_h("{} took {} damage!", [target.user_id, "1"])

    else:

        # Target's hp is < 12, nothing happens
        target.gc.tell_h("Your maximum hp ({}) is less than {}. Do nothing.", [
                         target.character.max_damage, "12"], target.socket_id)
        data = {'options': ['Do nothing']}
        target.gc.ask_h('confirm', data, target.user_id)
        target.gc.tell_h("{} did nothing.", [target.user_id])

def bully(args):

    # Choose a player to give the card to
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Hermit's Bully"]}, args['self'].user_id)
    target = args['self'].choosePlayer()
    display_data = args['card'].dump()
    display_data['type'] = 'draw'
    args['self'].gc.show_h(display_data, target.socket_id)

    # If target's hp is <= 11, they take 1 damage.
    if target.character.max_damage <= 11:

        # Prompt target to receive 1 damage
        target.gc.tell_h("Your maximum hp ({}) is {} or less.", [
                         target.character.max_damage, "11"], target.socket_id)
        data = {'options': ["Receive 1 damage"]}
        target.gc.ask_h('confirm', data, target.user_id)

        # Give 1 damage to target
        new_damage = target.moveDamage(-1, args['self'])
        target.gc.tell_h("{} took {} damage!", [target.user_id, "1"])

    else:

        # Target's hp is > 11, nothing happens
        target.gc.tell_h("Your maximum hp ({}) is greater than {}. Do nothing.", [
                         target.character.max_damage, "11"], target.socket_id)
        data = {'options': ['Do nothing']}
        target.gc.ask_h('confirm', data, target.user_id)
        target.gc.tell_h("{} did nothing.", [target.user_id])

def prediction(args):
    # Choose a player to give the card to
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Hermit's Prediction"]}, args['self'].user_id)
    target = args['self'].choosePlayer()
    display_data = args['card'].dump()
    display_data['type'] = 'draw'
    args['self'].gc.show_h(display_data, target.socket_id)

    # Prompt target to reveal themself
    target.gc.tell_h("You have no choice. Reveal yourself to {}.", [
                     args['self'].user_id], target.socket_id)
    data = {'options': ["Reveal"]}
    target.gc.ask_h('confirm', data, target.user_id)

    # Send target's information to user
    display_data = {'type': 'reveal', 'player': target.dump()}
    args['self'].gc.show_h(display_data, args['self'].socket_id)
    target.gc.tell_h("{} revealed their identity secretly to {}!", [
                     target.user_id, args['self'].user_id])
