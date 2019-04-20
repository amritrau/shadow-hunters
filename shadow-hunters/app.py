from flask import Flask, render_template, url_for, redirect, request, flash
from flask_socketio import SocketIO, join_room, leave_room
import random
import os
import re
from threading import Lock

from game_context import GameContext
from player import Player
import elements
from helpers import color_format, get_room_id

# app config
template_dir = os.path.abspath('./templates')
static_dir = os.path.abspath('./static')
app = Flask(
    __name__, template_folder=template_dir,
    static_folder=static_dir, static_url_path='/static'
)
app.config['SECRET_KEY'] = 'segfault hunters!'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
socketio = SocketIO(app, async_handlers=True)

# disable caching
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# sleep times after socket emissions (to pace frontend)
SOCKET_SLEEP = 0.25
AI_SLEEP = 2.0

# rooms are indexed by room_id, with a status, gc, and connections field
# status is LOBBY or GAME. gc is None if status is LOBBY, otherwise a
# GameContext object connections is a dict indexed by socket_id whose value is
# the username of that connection
rooms = {}

# Lock for manipulating the rooms data structure
connection_lock = Lock()

# APP ROUTES
@app.route('/')
def join():
    return render_template('join.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/room', methods=['GET', 'POST'])
def room(methods=['GET', 'POST']):
    if request.method == 'POST':

        # collect fields
        username = request.form.get('username').strip()
        room_id = request.form.get('room_id').strip()

        # check for valid characters in username and room id
        if not username or not room_id:
            flash("Please enter a name and room ID")
            return redirect('/')
        if len(username) >= 16 or len(room_id) >= 16:
            flash("Name and room ID must be shorter than 16 characters")
            return redirect('/')

        username_valid = re.match(r"^[\w\d ]*$", username)
        room_id_valid = re.match(r"^[\w\d ]*$", room_id)

        if (not username_valid) or (not room_id_valid):
            flash("Name and room ID must not contain special characters")
            return redirect('/')

        username_reserved = (username == "undefined") or username.isdigit()
        room_id_reserved = (room_id == "undefined") or room_id.isdigit()

        if username_reserved or room_id_reserved:
            flash("The username or room ID you chose is reserved.")
            return redirect('/')

        # Check for reserved usernames
        ef = elements.ElementFactory()
        all_cards = ef.WHITE_DECK.cards
        all_cards += ef.BLACK_DECK.cards
        all_cards += ef.GREEN_DECK.cards

        element_names = [c.title for c in all_cards]
        element_names += [ch.name for ch in ef.CHARACTERS]
        element_names += [a.name for a in ef.AREAS]

        name_reserved = username.startswith('CPU') or (username in element_names)
        if name_reserved or (username == 'Decline'):
            flash("The username you chose is reserved")
            return redirect('/')

        # check for username taken
        connection_lock.acquire()
        if (room_id in rooms) and username in rooms[room_id]['connections'].values():
            flash("Someone in the room has taken your name")
            connection_lock.release()
            return redirect('/')

        # check for game already in progress
        if (room_id in rooms) and rooms[room_id]['status'] == 'GAME':
            public_state, private_state = rooms[room_id]['gc'].dump()
            context = {
                'name': username,
                'room_id': room_id,
                'spectate': True,
                'reconnect': False,
                'gc_data': { 'public': public_state }
            }

            # Reconnect to game
            if username in rooms[room_id]['reconnections']:  # TODO: make actual browser cookie
                context['spectate'] = False
                context['reconnect'] = True
                context['gc_data']['private'] = [p for p in private_state if p['user_id'] == username][0]
                ai_player = [p for p in rooms[room_id]['gc'].players if p.user_id == username][0]
            connection_lock.release()
            return render_template('room.html', context=context)
        connection_lock.release()

        # send player to room
        return render_template('room.html', context={
            'name': username,
            'room_id': room_id,
            'spectate': False,
            'reconnect': False
        })
    else:
        return redirect('/')

# SOCKET EMITTERS


def socket_ask(form, data, user_id, room_id):

    # Get player
    connection_lock.acquire()
    if room_id in rooms:
        pl = [p for p in rooms[room_id]['gc'].players if p.user_id == user_id]
        player = pl[0]
    else:
        connection_lock.release()
        if 'Decline' in data['options'] and len(data['options']) > 1:
            data['options'].remove('Decline')
        return {'value': random.choice(data['options'])}
    connection_lock.release()

    # If player is a CPU, choose randomly from options
    if player.ai:
        socketio.sleep(AI_SLEEP)
        if 'Decline' in data['options'] and len(data['options']) > 1:
            data['options'].remove('Decline')
        return {'value': random.choice(data['options'])}

    # Otherwise, emit ask
    sid = player.socket_id
    bin = rooms[room_id]['gc'].answer_bin
    data['form'] = form
    bin['answered'] = False
    socketio.emit('ask', data, room=sid)

    # Loop until an answer is received
    while not bin['answered']:
        while not bin['answered']:
            # If a player swaps out for an AI during an ask, the AI answers
            # for them
            if player.ai or player.socket_id != sid:
                if 'Decline' in data['options'] and len(data['options']) > 1:
                    data['options'].remove('Decline')
                return {'value': random.choice(data['options'])}
            socketio.sleep(SOCKET_SLEEP)

        # Validate answerer and answer
        if bin['sid'] != sid or bin['data']['value'] not in data['options']:
            bin['answered'] = False

    # Return answer
    bin['answered'] = False
    return bin['data']


def socket_tell(str, args, gc, room_id, client=None):
    if not client:
        client = (room_id)
    data = color_format(str, args, gc)
    packet = {'strings': data[0], 'colors': data[1]}
    print(packet)
    print(client[0])
    socketio.emit('message', packet, room=client[0])
    if room_id in rooms:
        socketio.sleep(SOCKET_SLEEP)

def socket_show(data, gc, room_id, client=None):
    assert data['type'] in ["die", "win", "reveal", "roll", "draw"]
    if not client:
        client = (room_id)
    socketio.emit('display', data, room=client[0])
    if room_id in rooms:
        socketio.sleep(SOCKET_SLEEP)

def socket_update(data, room_id):
    socketio.emit('update', data, room=room_id)
    if room_id in rooms:
        socketio.sleep(SOCKET_SLEEP)

# SOCKET RECEIVERS

@socketio.on('start')
def on_start(json):

    # Get room and players in it
    connection_lock.acquire()
    room_id = get_room_id(rooms, request.sid)
    if not room_id:
        connection_lock.release()
        return

    people_in_room = rooms[room_id]['connections']
    names_and_sids = [(people_in_room[x], x) for x in people_in_room.keys()]

    # Check for false start
    n_players = max(min(int(json['n_players']), 8), 4)
    if len(names_and_sids) > n_players:
        connection_lock.release()
        packet = {'field': n_players, 'actual': len(names_and_sids)}
        socketio.emit('false_start', packet, room=request.sid)
        return

    # Initialize human and AI players
    rgb = ['rgb(245,245,245)', 'rgb(100,100,100)', 'rgb(79,182,78)', 'rgb(62,99,171)',
           'rgb(197,97,163)', 'rgb(219,62,62)', 'rgb(249,234,48)', 'rgb(239,136,43)']
    human_players = [Player(n[0], n[1], rgb.pop(0), False) for n in names_and_sids]
    ai_players = [Player("CPU_{}".format(i), str(i), rgb.pop(0), True) for i in range(1, n_players - len(human_players) + 1)]
    players = human_players + ai_players

    # Initialize game context with players and emission functions
    ef = elements.ElementFactory()
    gc = GameContext(
            players = players,
            characters = ef.CHARACTERS,
            black_cards = ef.BLACK_DECK,
            white_cards = ef.WHITE_DECK,
            green_cards = ef.GREEN_DECK,
            areas = ef.AREAS,
            ask_h = lambda x, y, z: socket_ask(x, y, z, room_id),
            tell_h = None,
            show_h = None,
            update_h = None
    )
    gc.tell_h = lambda x, y, *z: socket_tell(x, y, gc, room_id, z)
    gc.show_h = lambda x, *y: socket_show(x, gc, room_id, y)
    gc.update_h = lambda: socket_update(gc.dump()[0], room_id)

    # Assign game to room
    if rooms[room_id]['status'] == 'GAME':
        connection_lock.release()
        return
    rooms[room_id]['gc'] = gc
    rooms[room_id]['status'] = 'GAME'

    connection_lock.release()

    # Send public and private game states to frontend
    gc.tell_h("Started a game with players {}".format(", ".join(['{}']*len(players))), [p.user_id for p in players])
    public_state, private_state = gc.dump()
    for priv in private_state:
        data = {
            'public': public_state,
            'private': priv,
            'playable_chars': [ch.dump() for ch in gc.playable]
        }
        socketio.emit('game_start', data, room = priv['socket_id'])

    # Initiate gameplay loop
    gc.play()

@socketio.on('reveal')
def on_reveal():

    # Get room
    connection_lock.acquire()
    room_id = get_room_id(rooms, request.sid)

    # Make sure room and game still exist
    if room_id and rooms[room_id]['gc']:
        player = [p for p in rooms[room_id]['gc'].players if p.socket_id == request.sid][0]
    else:
        connection_lock.release()
        return

    # Reveal them (if they're alive and unrevealed)
    connection_lock.release()
    elements.reveal_lock.acquire()
    if player.state == 2:
        player.state = 1 # Guard
        elements.reveal_lock.release()
        player.reveal()


@socketio.on('special')
def on_special():

    # Get room
    connection_lock.acquire()
    room_id = get_room_id(rooms, request.sid)

    # Make sure room and game still exist
    if room_id and rooms[room_id]['gc']:
        player = [p for p in rooms[room_id]['gc'].players if p.socket_id == request.sid][0]
    else:
        connection_lock.release()
        return
    connection_lock.release()

    # Use special
    elements.reveal_lock.acquire()
    if not player.special_active:
        player.special_active = True
        elements.reveal_lock.release()
        player.character.special(rooms[room_id]['gc'], player, turn_pos = 'now')
        rooms[room_id]['gc'].update_h()

@socketio.on('answer')
def on_answer(json):

    # Make sure an answer isn't already being processed
    connection_lock.acquire()
    room_id = get_room_id(rooms, request.sid)
    if not room_id or rooms[room_id]['status'] != 'GAME' or rooms[room_id]['gc'].answer_bin['answered']:
        connection_lock.release()
        return
    bin = rooms[room_id]['gc'].answer_bin

    # Fill answer bin
    bin['data'] = json
    bin['sid'] = request.sid
    bin['answered'] = True
    connection_lock.release()

@socketio.on('message')
def on_message(json):

    # Message fields
    connection_lock.acquire()
    room_id = get_room_id(rooms, request.sid)
    if not room_id:
        connection_lock.release()
        return
    json['name'] = rooms[room_id]['connections'][request.sid]

    # If player is not in game, or spectating, their color is grey
    if (rooms[room_id]['status'] != 'GAME') or (request.sid not in [p.socket_id for p in rooms[room_id]['gc'].players]):
        json['color'] = elements.TEXT_COLORS['server']
    else:
        json['color'] = [p.color for p in rooms[room_id]['gc'].players if p.socket_id == request.sid][0]
    connection_lock.release()

    # Broadcast non-empty message
    if 'data' in json and json['data'].strip():
        socketio.emit('message', json, room=room_id)

@socketio.on('join')
def on_join(json):

    # Get fields
    room_id = json['room_id']
    name = json['name']
    reconnect = json['reconnect']
    spectate = json['spectate']

    # Tell everyone about the join
    msg = '{} has joined the room!'
    if spectate:
        msg = '{} has joined the room as a spectator!'
    elif reconnect:
        msg = '{} has rejoined the room!'
    socket_tell(msg, [name], None, room_id)

    # Create room if it doesn't exist and add player to room
    connection_lock.acquire()
    if room_id not in rooms:
        if spectate or reconnect:
            connection_lock.release()
            socketio.disconnect(request.sid)
            return
        rooms[room_id] = {'status': 'LOBBY', 'gc': None, 'connections': {}, 'reconnections': {}}

    # If this is a reconnection event, change player's socket id and AI status in game context
    if reconnect:
        del rooms[room_id]['reconnections'][name]
        player = [p for p in rooms[room_id]['gc'].players if p.user_id == name][0]
        player.socket_id = request.sid
        player.ai = False

    # Add new player to room
    rooms[room_id]['connections'][request.sid] = name
    join_room(room_id)
    connection_lock.release()

    # Emit welcome message to new player
    msg = 'Welcome to Shadow Hunters Room: '+room_id
    if json['spectate']:
        msg = 'You are now spectating Shadow Hunters Room: '+room_id
    if not reconnect:
        socket_tell(msg, [], None, room_id, client=(request.sid,))

    # Tell player about other room members
    members = [x for x in rooms[room_id]['connections'].values() if x != name]
    msg = 'There\'s no one else here!'
    if members:
        msg = 'Other players in the room: '+', '.join(members)
    if not reconnect:
        socket_tell(msg, [], None, room_id, client=(request.sid,))

@socketio.on('disconnect')
def on_disconnect():

    # Get room_id, name, and game context
    room_id = get_room_id(rooms, request.sid)
    name = rooms[room_id]['connections'][request.sid]
    gc = rooms[room_id]['gc']
    socket_tell('{} has left the room', [name], gc, room_id)

    # Remove user from the room
    connection_lock.acquire()
    rooms[room_id]['connections'].pop(request.sid)

    # Close room if it is now empty, or replace player with AI if it's in game
    if not rooms[room_id]['connections'].keys():

        # Close the room
        if gc and [p for p in gc.players if p.socket_id == request.sid]:
            [p for p in gc.players if p.socket_id == request.sid][0].ai = True
        socketio.close_room(room_id)
        rooms.pop(room_id)
        connection_lock.release()

    elif gc and not gc.game_over:

        # If disconnected person was spectating, or dead, or if the game is over,
        # don't swap them for an AI
        player_in_game = [p for p in gc.players if p.socket_id == request.sid]
        if (not player_in_game) or (not player_in_game[0].state):
            connection_lock.release()
            return

        # Swap player for AI
        player_in_game[0].ai = True
        rooms[room_id]['reconnections'][player_in_game[0].user_id] = 'cookie' # TODO: make actual browser cookie
        connection_lock.release()
        socket_tell('A computer player has taken their place!', [], gc, room_id)

    else:

        # Always release lock!
        connection_lock.release()

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
