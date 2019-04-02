from flask import Flask, render_template, url_for, redirect, request, flash
from flask_socketio import SocketIO, join_room, leave_room
import random
import string
import os
import re

from game_context import GameContext
from player import Player
import elements

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
S_COLOR = 'rgb(37,25,64)'

# connection/room management data structures
connections = {}
rooms = {}
get_sid = {}
answer_bins = {
    'answered': False,
    'sid': '',
    'form': '',
    'data': {}
}

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

        # check for valid username and room id
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

def start_game(room_id, names):

    # Initialize human and AI players
    n_players = 5 # random.randrange(max(len(names), 4), 9, 1) ## TODO Replace with dropdown response
    human_players = [Player(n, get_sid[(n, room_id)], lambda x, y, z: server_ask(x, y, z, room_id), False) for n in names]
    ai_players = [Player("CPU_{}".format(i), str(i), ai_ask, True) for i in range(1, n_players - len(human_players) + 1)]
    players = human_players + ai_players


    # Initialize game context with players and match room with game context
    ef = elements.ElementFactory()
    gc = GameContext(
            players = players,
            characters = ef.CHARACTERS,
            black_cards = ef.BLACK_DECK,
            white_cards = ef.WHITE_DECK,
            green_cards = ef.GREEN_DECK,
            areas = ef.AREAS,
            tell_h = lambda x: server_msg(x, room_id),
            direct_h = lambda x, sid: server_msg(x, sid),
            update_h = lambda x: server_update(x, room_id)
    )
    gc.update_h = lambda: server_update(gc.dump()[0], room_id)
    rooms[room_id]['gc'] = gc

    gc.tell_h(
        "Started a game with players {}".format(", ".join([p.user_id for p in players])))

    # Fix hermit tests
    # Write single use tests
    # change tell_h and direct_h to have type json
    # reveals (backend, then frontend)

    # Send public and private game states to frontend
    public_state, private_state = gc.dump()
    for k in private_state:
        data = {'public': public_state, 'private': private_state[k], 'playable_chars': [ch.dump() for ch in gc.playable]}
        socketio.emit('game_start', data, room = k)

    # Initiate gameplay loop
    winners = gc.play()

    # Send winners to frontend in socket emission for game-over screen
    # TODO

def server_ask(form, data, user_id, room_id):

    # Emit ask
    sid = get_sid[(user_id, room_id)]
    player = [p for p in rooms[room_id]['gc'].players if p.socket_id == sid][0]
    data['form'] = form
    answer_bins[room_id]['answered'] = False
    socketio.emit('ask', data, room=sid)

    # Loop until an answer is received
    while not answer_bins[room_id]['answered']:
        while not answer_bins[room_id]['answered']:
            # If a player swaps out for an AI during an ask, the AI answers for them
            if player.ai:
                return {'value': random.choice(data['options'])}
            socketio.sleep(SOCKET_SLEEP)

        # Validate answerer and answer
        if (answer_bins[room_id]['sid'] != sid or answer_bins[room_id]['form'] != form
        or answer_bins[room_id]['data']['value'] not in data['options']):
            answer_bins[room_id]['answered'] = False

    # Return answer
    answer_bins[room_id]['answered'] = False
    return answer_bins[room_id]['data']

def ai_ask(x, y, z):
    socketio.sleep(AI_SLEEP)
    return {'value': random.choice(y['options'])}

def server_msg(data, room_id):
    socketio.emit('message', {'data': data, 'color': S_COLOR}, room=room_id)
    socketio.sleep(SOCKET_SLEEP)

def server_update(data, room_id):
    socketio.emit('update', data, room=room_id)
    socketio.sleep(SOCKET_SLEEP)

# SOCKET HANDLERS

@socketio.on('start')
def on_start():

    # Mark game as in progress so no one else can start it
    room_id = connections[request.sid]['room_id']
    if rooms[room_id]['status'] == 'GAME':
        return
    rooms[room_id]['status'] = 'GAME'

    # Set default values for this room's answer bin
    answer_bins[room_id] = {
        'answered': False,
        'sid': '',
        'form': '',
        'data': {}
    }

    # Begin game
    names = [x['name'] for x in connections.values() if x['room_id'] == room_id]
    socketio.sleep(SOCKET_SLEEP)
    start_game(room_id, names)

@socketio.on('reveal')
def on_reveal():

    # Get info about user in game
    room_id = connections[request.sid]['room_id']
    gc = rooms[room_id]['gc']
    player = [p for p in gc.players if p.socket_id == request.sid][0]

    # Reveal them
    player.reveal()

@socketio.on('answer')
def on_answer(json):

    # Make sure an answer isn't already being processed
    room_id = connections[request.sid]['room_id']
    if answer_bins[room_id]['answered']:
        return

    # Fill answer bin
    answer_bins[room_id]['form'] = json.pop('form', None)
    answer_bins[room_id]['data'] = json
    answer_bins[room_id]['sid'] = request.sid
    answer_bins[room_id]['answered'] = True

@socketio.on('message')
def on_message(msg):

    # Broadcast message to all players
    room_id = connections[request.sid]['room_id']
    msg['name'] = connections[request.sid]['name']
    msg['color'] = connections[request.sid]['color']
    socketio.emit('message', msg, room=room_id)

@socketio.on('join')
def on_join(json):

    # Add new player to active connections
    room_id = json['room_id']
    name = json['name']
    rgb = [str(random.randint(25,150)), str(random.randint(25,150)), str(random.randint(25,150))]
    connections[request.sid] = { 'name': name, 'room_id': room_id }
    connections[request.sid]['color'] = 'rgb('+rgb[0]+','+rgb[1]+','+rgb[2]+')'
    get_sid[(name, room_id)] = request.sid

    # Emit join message to other players
    join_msg = name+' has joined the room!'
    if json['spectate']:
        join_msg = name+' has joined the room as a spectator!'
    data = {'data': join_msg, 'color': S_COLOR}
    socketio.emit('message', data, room=room_id)

    # Join room
    join_room(room_id)

    # Emit welcome message to new player
    join_msg = 'Welcome to Shadow Hunters Room: '+room_id
    if json['spectate']:
        join_msg = 'You are now spectating Shadow Hunters Room: '+room_id
    data = {'data': join_msg, 'color': S_COLOR}
    socketio.emit('message', data, room=request.sid)

    # Tell player about other room members
    members = [x['name'] for x in connections.values() if (x['room_id'] == room_id and x['name'] != name)]
    msg = 'There\'s no one else here!'
    if members:
        msg = 'Other players in the room: '+', '.join(members)
    data = {'data': msg, 'color': S_COLOR}
    socketio.emit('message', data, room=request.sid)

@socketio.on('disconnect')
def on_disconnect():

    # Tell everyone in the room about the disconnect
    name = connections[request.sid]['name']
    room_id = connections[request.sid]['room_id']
    socketio.emit('message', {'data': name+' has left the room', 'color': S_COLOR}, room=room_id)

    # Remove user from all connection data structures
    connections.pop(request.sid)
    get_sid.pop((name, room_id))

    # Close room if it is now empty, or replace player with AI if it's in game
    if len([x for x in connections.values() if x['room_id'] == room_id]) == 0:

        # Close the room
        socketio.close_room(room_id)
        rooms.pop(room_id)

    elif rooms[room_id]['status'] == 'GAME' and (not rooms[room_id]['gc'].game_over):

        # If disconnected person was spectating, or dead, or if the game is over,
        # don't swap them for an AI
        player_in_game = [p for p in rooms[room_id]['gc'].players if p.socket_id == request.sid]
        if (not player_in_game) or (not player_in_game[0].state):
            return

        # Swap player for AI
        player = player_in_game[0]
        player.user_id = 'CPU_{}'.format(name)
        player.ask_h = ai_ask
        player.ai = True

        # Tell everyone about the swap
        msg = 'A computer player, {} has taken {}\'s place!'.format(player.user_id, name)
        socketio.emit('message', {'data': msg, 'color': S_COLOR}, room=room_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=80)
