# area.py
# Implements a Area.


class Area:
    def __init__(self, name, desc, domain, action, resource_id):
        self.name = name
        self.desc = desc
        self.zone = None
        self.domain = domain
        self.action = action
        self.resource_id = resource_id

    def getAdjacent(self):
        return [a for a in self.zone.areas if a != self][0]

    def dump(self):
        return {
            'name': self.name,
            'desc': self.desc,
            'domain': str(self.domain)
        }

    def __str__(self):
        return str(self.dump())


# Area actions
def underworld_gate_action(gc, player):

    # Ask player which deck to draw from
    data = {'options': ["Draw White Card",
                        "Draw Black Card", "Draw Hermit Card"]}
    answer = player.gc.ask_h('select', data, player.user_id)['value']

    # Draw from corresponding deck
    if answer == "Draw White Card":
        player.drawCard(gc.white_cards)
    elif answer == "Draw Black Card":
        player.drawCard(gc.black_cards)
    else:
        player.drawCard(gc.green_cards)

def weird_woods_action(gc, player):

    # Choose which player to attack or heal
    target_Player = player.choosePlayer(include_self=True)

    # Choose whether to attack or heal
    data = {'options': ["Heal 1 damage", "Give 2 damage"]}
    amount = player.gc.ask_h('select', data, player.user_id)['value']
    if amount == "Heal 1 damage":
        gc.tell_h("The power of the {} healed {}!", [
                  "Weird Woods", target_Player.user_id])
        target_Player.moveDamage(1, player)
    else:
        if target_Player.hasEquipment("Fortune Brooch"):
            gc.tell_h("{}'s {} protected them from damage!", [
                      target_Player.user_id, "Fortune Brooch"])
        else:
            gc.tell_h("The power of the {} damaged {}!", [
                      "Weird Woods", target_Player.user_id])
            target_Player.moveDamage(-2, player)

def erstwhile_altar_action(gc, player):

    # Get players who have equipment
    players_w_items = [p for p in gc.getLivePlayers() if (
        len(p.equipment) and p != player)]

    # If someone has equipment to steal and isn't current player, offer choice
    if len(players_w_items):

        # Choose player to steal from
        data = {'options': [p.user_id for p in players_w_items]}
        target = player.gc.ask_h(
            'select', data, player.user_id)['value']
        target_Player = [
            p for p in players_w_items if p.user_id == target][0]

        # Choose equipment to take from player
        data = {'options': [
            eq.title for eq in target_Player.equipment]}
        equip = player.gc.ask_h(
            'select', data, player.user_id)['value']
        equip_Equipment = [
            eq for eq in target_Player.equipment if eq.title == equip][0]

        # Transfer equipment from one player to the other
        target_Player.giveEquipment(player, equip_Equipment)

    else:

        # If no one has equipment to steal, nothing happens
        gc.tell_h("Nobody has any items for {} to steal.",
                  [player.user_id])
