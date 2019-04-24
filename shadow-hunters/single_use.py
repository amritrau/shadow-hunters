# single_use.py
# card.use(args) function implementations.

# White single-use cards

def first_aid(args):
    """Select a player to use card on (includes user)"""

    args['self'].gc.ask_h('confirm', {'options': ["Use First Aid"]}, args['self'].user_id)
    target_Player = args['self'].choosePlayer(include_self=True)
    target_Player.setDamage(7, args['self'])
    args['self'].gc.tell_h("{} applied {} to {}!", [args['self'].user_id, args['card'].title, target_Player.user_id])

def judgement(args):
    """Give all players except user 2 damage"""

    args['self'].gc.ask_h('confirm', {'options': ["Unleash judgement"]}, args['self'].user_id)
    for p in args['self'].gc.getLivePlayers(lambda x: (x != args['self'])):
        p.moveDamage(-2, args['self'])

def holy_water(args):
    """Heal user by 2 damage"""

    args['self'].gc.ask_h('confirm', {'options': ["Heal yourself"]}, args['self'].user_id)
    args['self'].moveDamage(2, args['self'])

def advent(args):
    """If hunter, can reveal and heal fully, or heal fully if already revealed"""

    data = {'options': ["Do nothing"]}
    if args['self'].character.alleg == 2:
        if args['self'].state == 2:
            data['options'].append("Reveal and heal fully")
        else:
            data['options'].append("Heal fully")

    # Get decision and take corresponding action
    decision = args['self'].gc.ask_h(
        'yesno', data, args['self'].user_id)['value']
    if decision == "Do nothing":
        args['self'].gc.tell_h("{} did nothing.", [args['self'].user_id])
    elif decision == "Reveal and heal fully":
        args['self'].reveal()
        args['self'].setDamage(0, args['self'])
    else:
        args['self'].setDamage(0, args['self'])

def disenchant_mirror(args):
    """If shadow and not unknown, force reveal"""

    data = {'options': ["Do nothing"]}
    if args['self'].character.alleg == 0 and args['self'].character.name != "Unknown":
        data = {'options': ["Reveal yourself"]}

    # Reveal character, or do nothing if hunter
    decision = args['self'].gc.ask_h('yesno', data, args['self'].user_id)['value']
    if decision == "Do nothing":
        args['self'].gc.tell_h("{} did nothing.", [args['self'].user_id])
    else:
        args['self'].reveal()

def blessing(args):
    """Heal player by rolling 6-sided die"""

    # Choose a player to use blessing on
    args['self'].gc.ask_h('confirm', {'options': ["Bless someone"]}, args['self'].user_id)
    target = args['self'].choosePlayer()

    # Roll dice to get value to heal by
    roll_result = args['self'].rollDice('6')

    # Heal target player
    target.moveDamage(roll_result, args['self'])
    args['self'].gc.tell_h("The blessing healed {}!", [target.user_id])

def chocolate(args):
    """If low-hp character, can reveal and heal fully, or heal fully if already revealed"""

    data = {'options': ["Do nothing"]}
    if args['self'].character.name in ["Allie", "Agnes", "Emi", "Ellen", "Ultra Soul", "Unknown"]:
        if args['self'].state == 2:
            data['options'].append("Reveal and heal fully")
        else:
            data['options'].append("Heal fully")

    # Get decision and take corresponding action
    decision = args['self'].gc.ask_h('yesno', data, args['self'].user_id)['value']
    if decision == "Do nothing":
        args['self'].gc.tell_h("{} did nothing.", [args['self'].user_id])
    elif decision == "Reveal and heal fully":
        args['self'].reveal()
        args['self'].setDamage(0, args['self'])
    else:
        args['self'].setDamage(0, args['self'])

def concealed_knowledge(args):
    """Change turn order so that current player goes again"""

    args['self'].gc.ask_h('confirm', {'options': ["Use Concealed Knowledge"]}, args['self'].user_id)
    args['self'].gc.turn_order.insert(args['self'].gc.turn_order.index(args['self']), args['self'])

def guardian_angel(args):
    """User can't take damage until their next turn - this is checked in player.defend() and player.takeTurn()"""

    args['self'].gc.ask_h('confirm', {'options': ["Summon a Guardian Angel"]}, args['self'].user_id)
    args['self'].modifiers['guardian_angel'] = True

# Black single-use cards
def bloodthirsty_spider(args):
    """Both the target and the user take 2 damage"""

    # Choose a player to attack
    args['self'].gc.ask_h(
        'confirm', {'options': ["Summon a Bloodthirsty Spider"]}, args['self'].user_id)
    target = args['self'].choosePlayer()

    if target.hasEquipment("Talisman"):
        args['self'].gc.tell_h("{}'s {} protected them from damage!", [
                               target.user_id, "Talisman"])
    else:
        target.moveDamage(-2, args['self'])
    args['self'].moveDamage(-2, args['self'])

def vampire_bat(args):
    """Target takes 2 damage, user heals 1 damage"""
    # Choose a player to attack
    args['self'].gc.ask_h(
        'confirm', {'options': ["Summon a Vampire Bat"]}, args['self'].user_id)
    target = args['self'].choosePlayer()

    if target.hasEquipment("Talisman"):
        args['self'].gc.tell_h("{}'s {} protected them from damage!", [
                               target.user_id, "Talisman"])
    else:
        target.moveDamage(-2, args['self'])
        args['self'].moveDamage(1, args['self'])

def moody_goblin(args):
    """Steal equipment from players"""

    # Show confirmation
    args['self'].gc.ask_h('confirm', {'options': ["Steal an Equipment Card"]}, args['self'].user_id)
    target_Player = args['self'].choosePlayer(filter_fn=lambda x: len(x.equipment))
    if target_Player:
        equip_Equipment = args['self'].chooseEquipment(target_Player)
        target_Player.giveEquipment(args['self'], equip_Equipment)
    else:
        args['self'].gc.tell_h("Nobody has any items for {} to steal.", [args['self'].user_id])

def diabolic_ritual(args):
    """If shadow, can reveal and heal fully"""

    data = {'options': ["Do nothing"]}
    if args['self'].character.alleg == 0 and args['self'].state != 1:
        data['options'].append("Reveal and heal fully")

    # Get decision and take corresponding action
    decision = args['self'].gc.ask_h('yesno', data, args['self'].user_id)['value']
    if decision == "Do nothing":
        args['self'].gc.tell_h("{} did nothing.", [args['self'].user_id])
    else:
        args['self'].reveal()
        args['self'].setDamage(0, args['self'])

def banana_peel(args):
    """If have equipment, must give away one or take damage. If no equipment, must take damage"""

    if len(args['self'].equipment):
        data = {'options': ["Give an equipment card", "Receive 1 damage"]}
    else:
        data = {'options': ["Receive 1 damage"]}

    # Get decision and take action
    decision = args['self'].gc.ask_h('yesno', data, args['self'].user_id)['value']
    if decision == "Give an equipment card":
        # Choose an equipment card to give away
        args['self'].gc.tell_h("{} is choosing an equipment card to give away...", [args['self'].user_id])
        eq = args['self'].chooseEquipment(args['self'])

        # Give away equipment
        receiver = args['self'].choosePlayer()
        args['self'].giveEquipment(receiver, eq)

    else:
        # Take 1 damage
        args['self'].moveDamage(-1, args['self'])
        args['self'].gc.tell_h("{} took {} damage.", [args['self'].user_id, "1"])

def dynamite(args):
    """Hit all players in area for 3 damage"""

    # Roll to find out which area gets hit
    args['self'].gc.ask_h(
        'confirm', {'options': ["Light the fuse"]}, args['self'].user_id)
    args['self'].gc.tell_h("{} is rolling for where the dynamite lands...", [
                           args['self'].user_id])
    roll_result = args['self'].rollDice('area')

    # Hit area corresponding to roll number
    if roll_result == 7:
        # No area has 7 on it
        args['self'].gc.tell_h("Nothing happens.", [])

    else:
        # Get area from roll result
        destination_Area = args['self'].gc.getAreaFromRoll(roll_result)
        destination = destination_Area.name

        # Hit all players in area for 3 damage
        args['self'].gc.tell_h("{} blew up the {}!", ["Dynamite", destination])
        affected_players = args['self'].gc.getPlayersAt(destination)
        for p in affected_players:
            if p.hasEquipment("Talisman"):
                args['self'].gc.tell_h("{}'s {} protected them from damage!", [p.user_id, "Talisman"])
            else:
                p.moveDamage(-3, args['self'])

def spiritual_doll(args):
    """If roll is >= 5, user takes 3 damage. Otherwise, target takes 3 damage."""

    # Choose a player to target
    args['self'].gc.ask_h(
        'confirm', {'options': ["Use Spiritual Doll"]}, args['self'].user_id)
    target = args['self'].choosePlayer()

    # Roll 6-sided die
    roll_result = args['self'].rollDice('6')

    # If roll is >= 5, user takes 3 damage. Otherwise, target takes 3 damage.
    if roll_result >= 5:
        args['self'].moveDamage(-3, args['self'])
        args['self'].gc.tell_h('The {} backfired on {}!', [
                               args['card'].title, args['self'].user_id])
    else:
        target.moveDamage(-3, args['self'])
        args['self'].gc.tell_h('The {} cursed {}!', [
                               args['card'].title, target.user_id])
