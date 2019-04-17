from flask import Flask, render_template, url_for, redirect, request, flash
from flask_socketio import SocketIO, join_room, leave_room
import random
import string
import os
import re

from game_context import GameContext
from player import Player
import elements
from helpers import color_format

# basic app setup
template_dir = os.path.abspath('./templates')
static_dir = os.path.abspath('./static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='/static')
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

# constants
SOCKET_SLEEP = 0.25
AI_SLEEP = 3.0

# connection/room management data structures
connections = {}
rooms = {}
get_sid = {}

# APP ROUTES

@app.route('/')
def join():
    return render_template('join.html')

@app.route('/room', methods=['GET', 'POST'])
def room(methods=['GET','POST']):
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
        if (not re.match("^[\w\d ]*$", username)) or (not re.match("^[\w\d ]*$", room_id)):
            flash("Name and room ID must not contain special characters")
            return redirect('/')
        if username == "undefined" or room_id == "undefined":
            flash("Nice try.")
            return redirect('/')

        # Check for reserved usernames
        ef = elements.ElementFactory()
        all_cards = ef.WHITE_DECK.cards + ef.BLACK_DECK.cards + ef.GREEN_DECK.cards
        element_names = [c.title for c in all_cards] + [ch.name for ch in ef.CHARACTERS] + [a.name for a in ef.AREAS]
        if username.isdigit() or username.startswith('CPU') or username in element_names or username == 'Decline':
            flash("The username you chose is reserved")
            return redirect('/')

        # check for username taken
        if (username, room_id) in get_sid:
            flash("Someone in the room has taken your name")
            return redirect('/')

        # check for game already in progress
        if room_id in rooms and rooms[room_id]['status'] == 'GAME':
            public_state, private_state = rooms[room_id]['gc'].dump()
            return render_template('room.html', context = {
                'name': username,
                'room_id': room_id,
                'spectate': True,
                'gc_data': { 'public': public_state }
            })

        # send player to room
        rooms[room_id] = {'status': 'LOBBY', 'gc': None}
        return render_template('room.html', context={ 'name': username, 'room_id': room_id, 'spectate': False })
    else:
        return redirect('/')

# GAMEPLAY FUNCTIONS

def start_game(room_id, names, n_players):

    # Initialize human and AI players
    rgb = ['rgb(255,255,255)', 'rgb(100,100,100)', 'rgb(79,182,78)', 'rgb(62,99,171)',
           'rgb(197,97,163)', 'rgb(219,62,62)', 'rgb(249,234,48)', 'rgb(239,136,43)']
    human_players = [Player(n, get_sid[(n, room_id)], rgb.pop(0), False) for n in names]
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
    gc.tell_h = lambda x, y, *z: socket_tell(x, y, gc, room_id, client=z)
    gc.show_h = lambda x, *y: socket_show(x, gc, room_id, client=y)
    gc.update_h = lambda: socket_update(gc.dump()[0], room_id)

    # Assign game to room
    if rooms[room_id]['status'] == 'GAME':
        return
    rooms[room_id]['gc'] = gc
    rooms[room_id]['status'] = 'GAME'

    # Send public and private game states to frontend
    gc.tell_h("Started a game with players {}".format(", ".join([p.user_id for p in players])), [])
    public_state, private_state = gc.dump()
    for k in private_state:
        data = {'public': public_state, 'private': private_state[k], 'playable_chars': [ch.dump() for ch in gc.playable]}
        socketio.emit('game_start', data, room = k)

    # Initiate gameplay loop
    gc.play()

def socket_ask(form, data, user_id, room_id):

    # Get player and socket id
    player = [p for p in rooms[room_id]['gc'].players if p.user_id == user_id][0]

    # If player is a CPU, choose randomly from options
    if player.ai:
        socketio.sleep(AI_SLEEP)
        return {'value': random.choice(data['options'])}

    # Otherwise, emit ask
    sid = get_sid[(user_id, room_id)]
    bin = rooms[room_id]['gc'].answer_bin
    data['form'] = form
    bin['answered'] = False
    socketio.emit('ask', data, room=sid)

    # Loop until an answer is received
    while not bin['answered']:
        while not bin['answered']:
            # If a player swaps out for an AI during an ask, the AI answers for them
            if player.ai:
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
    socketio.emit('message', {'strings': data[0], 'colors': data[1]}, room=client[0])
    socketio.sleep(SOCKET_SLEEP)

def socket_show(data, gc, room_id, client=None):
    assert data['type'] in ["die", "win", "reveal", "roll", "draw"]
    if not client:
        client = (room_id)
    socketio.emit('display', data, room=client[0])
    socketio.sleep(SOCKET_SLEEP)

def socket_update(data, room_id):
    socketio.emit('update', data, room=room_id)
    socketio.sleep(SOCKET_SLEEP)

# SOCKET HANDLERS

@socketio.on('start')
def on_start(json):

    # Get room
    room_id = connections[request.sid]['room_id']

    # Get number of players
    n_players = max(min(int(json['n_players']), 8), 4)
    names = [x['name'] for x in connections.values() if x['room_id'] == room_id]
    if len(names) > n_players:
        socketio.emit('false_start', {'field':n_players, 'actual':len(names)}, room=request.sid)
        return

    # Begin game
    socketio.sleep(SOCKET_SLEEP)
    start_game(room_id, names, n_players)

@socketio.on('reveal')
def on_reveal():

    # Get info about user in game
    room_id = connections[request.sid]['room_id']
    gc = rooms[room_id]['gc']
    player = [p for p in gc.players if p.socket_id == request.sid][0]

    # Reveal them (if they're alive and unrevealed)
    if player.state == 2:
        player.reveal()

@socketio.on('answer')
def on_answer(json):

    # Make sure an answer isn't already being processed
    room_id = connections[request.sid]['room_id']
    if rooms[room_id]['status'] != 'GAME' or rooms[room_id]['gc'].answer_bin['answered']:
        return
    bin = rooms[room_id]['gc'].answer_bin

    # Fill answer bin
    bin['data'] = json
    bin['sid'] = request.sid
    bin['answered'] = True

@socketio.on('message')
def on_message(json):

    # Message fields
    room_id = connections[request.sid]['room_id']
    json['name'] = connections[request.sid]['name']

    # If player is not in game, or spectating, their color is grey
    if (rooms[room_id]['status'] != 'GAME') or (request.sid not in [p.socket_id for p in rooms[room_id]['gc'].players]):
        json['color'] = elements.TEXT_COLORS['s']
    else:
        json['color'] = [p.color for p in rooms[room_id]['gc'].players if p.socket_id == request.sid][0]

    # Broadcast non-empty message
    if 'data' in json and json['data'].strip():
        socketio.emit('message', json, room=room_id)

@socketio.on('join')
def on_join(json):

    # Add new player to active connections
    room_id = json['room_id']
    name = json['name']
    connections[request.sid] = { 'name': name, 'room_id': room_id }
    connections[request.sid]['color'] = elements.TEXT_COLORS['s']
    get_sid[(name, room_id)] = request.sid

    # Emit join message to other players
    join_msg = name+' has joined the room!'
    if json['spectate']:
        join_msg = name+' has joined the room as a spectator!'
    socket_tell(join_msg, [], None, room_id)

    # Join room
    join_room(room_id)

    # Emit welcome message to new player
    join_msg = 'Welcome to Shadow Hunters Room: '+room_id
    if json['spectate']:
        join_msg = 'You are now spectating Shadow Hunters Room: '+room_id
    socket_tell(join_msg, [], None, room_id)

    # Tell player about other room members
    members = [x['name'] for x in connections.values() if (x['room_id'] == room_id and x['name'] != name)]
    msg = 'There\'s no one else here!'
    if members:
        msg = 'Other players in the room: '+', '.join(members)
    socket_tell(msg, [], None, room_id)

@socketio.on('disconnect')
def on_disconnect():

    # Tell everyone in the room about the disconnect
    name = connections[request.sid]['name']
    room_id = connections[request.sid]['room_id']
    gc = None
    if rooms[room_id]['status'] == 'GAME':
        gc = rooms[room_id]['gc']
    socket_tell('{} has left the room', [name], gc, room_id)

    # Remove user from all connection data structures
    connections.pop(request.sid)
    get_sid.pop((name, room_id))

    # Close room if it is now empty, or replace player with AI if it's in game
    if len([x for x in connections.values() if x['room_id'] == room_id]) == 0:

        # Close the room
        socketio.close_room(room_id)
        rooms.pop(room_id)

    elif gc and not gc.game_over:

        # If disconnected person was spectating, or dead, or if the game is over,
        # don't swap them for an AI
        player_in_game = [p for p in rooms[room_id]['gc'].players if p.socket_id == request.sid]
        if (not player_in_game) or (not player_in_game[0].state):
            return

        # Swap player for AI
        player = player_in_game[0]
        player.user_id = 'CPU_{}'.format(name)
        player.ai = True

        # Tell everyone about the swap
        socket_tell('A computer player, {} has taken their place!', [player.user_id], gc, room_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=80)
