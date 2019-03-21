from flask import Flask, render_template, url_for, redirect, request, flash
from flask_socketio import SocketIO, join_room, leave_room
from random import randint
from time import sleep
import os
from pprint import pprint  # TODO FOR TESTING PURPOSES ONLY, REMOVE!

from game_context import GameContext
from player import Player
import cli

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

        # form validation
        username = request.form.get('username').strip()
        room_id = request.form.get('room_id').strip()
        if not username or not room_id:
            flash("Please enter a username and room")
            return redirect('/')

        # don't let someone in if there's a game in progress in the room
        if room_id in rooms and rooms[room_id] == 'GAME':
            flash("This room is already in game")
            return redirect('/')

        # don't let someone enter a room with the same name as someone else
        if (username, room_id) in get_sid:
            flash("Someone in the room has taken your username")
            return redirect('/')

        # send them to join the room!
        rooms[room_id] = 'LOBBY'
        return render_template('room.html', context={ 'name': username, 'room_id': room_id })
    else:
        return redirect('/')

# GAMEPLAY FUNCTIONS

def start_game(room_id, players):

    # Initialize players and game context
    players = [Player(user_id, socket_id = get_sid[(user_id, room_id)]) for user_id in players]
    ef = cli.ElementFactory()
    gc = GameContext(
            players = players,
            characters = ef.CHARACTERS,
            black_cards = ef.BLACK_DECK,
            white_cards = ef.WHITE_DECK,
            green_cards = ef.GREEN_DECK,
            areas = ef.AREAS,
            tell_h = lambda x: server_msg(x, room_id),
            direct_h = lambda x, sid: server_msg(x, sid),
            ask_h = lambda x, y, z: server_ask(x, y, z, room_id),
            update_h = lambda x: server_update(x, room_id)
        )

    gc.update_h = lambda: server_update(gc.dump()[0], room_id)

    # gc.dump() can be called at any time to return a tuple of public,
    # private state. The public state is a self-explanatory dictionary; the
    # private state is keyed by socket_id (not by user_id!). This makes it
    # easier to send messages individually.

    # Send public and private game states across
    public_state, private_state = gc.dump()
    # socketio.emit('game_start', public_state, room = room_id)
    for k in private_state:
        data = {'public': public_state, 'private': private_state[k]}
        socketio.emit('game_start', data, room = k)

    # Initiate gameplay loop
    winners = gc.play()

def server_ask(form, data, player, room_id):
    # TODO Consider moving this to separate file

    # Emit ask
    sid = get_sid[(player, room_id)]
    data['form'] = form
    answer_bins[room_id]['answered'] = False
    socketio.emit('ask', data, room=sid)

    # Loop until an answer is received
    while not answer_bins[room_id]['answered']:
        while not answer_bins[room_id]['answered']:
            socketio.sleep(SOCKET_SLEEP)

        # Validate answerer and answer
        if (answer_bins[room_id]['sid'] != sid or answer_bins[room_id]['form'] != form
        or answer_bins[room_id]['data']['value'] not in data['options']):
            answer_bins[room_id]['answered'] = False

    # Return answer
    answer_bins[room_id]['answered'] = False
    return answer_bins[room_id]['data']

def server_msg(data, room_id):
    # TODO Consider moving this to separate file
    socketio.emit('message', {'data': data, 'color': S_COLOR}, room=room_id)
    socketio.sleep(SOCKET_SLEEP)

def server_update(data, room_id):
    # TODO Consider moving this to separate file
    socketio.emit('update', data, room=room_id)
    socketio.sleep(SOCKET_SLEEP)

# SOCKET HANDLERS

@socketio.on('start')
def on_start():

    # Mark game as in progress so no one else can start/join it
    room_id = connections[request.sid]['room_id']
    if rooms[room_id] == 'GAME':
        return
    rooms[room_id] = 'GAME'

    # Set default values for this room's answer bin
    answer_bins[room_id] = {
        'answered': False,
        'sid': '',
        'form': '',
        'data': {}
    }

    # Begin game
    players = [x['name'] for x in connections.values() if x['room_id'] == room_id]
    socketio.sleep(SOCKET_SLEEP)
    start_game(room_id, players)

@socketio.on('answer')
def on_answer(json):

    # Make sure an answer isn't being processed
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
    room_id = connections[request.sid]['room_id']
    msg['name'] = connections[request.sid]['name']
    msg['color'] = connections[request.sid]['color']
    socketio.emit('message', msg, room=room_id)

@socketio.on('join')
def on_join(json):

    # Add new player to active connections
    room_id = json['room_id']
    name = json['name']
    rgb = [str(randint(25,150)), str(randint(25,150)), str(randint(25,150))]
    connections[request.sid] = { 'name': name, 'room_id': room_id }
    connections[request.sid]['color'] = 'rgb('+rgb[0]+','+rgb[1]+','+rgb[2]+')'
    get_sid[(name, room_id)] = request.sid

    # Emit join message to other players
    data = {'data': name+' has joined Shadow Hunters Room: '+room_id, 'color': S_COLOR}
    socketio.emit('message', data, room=room_id)

    # Join room
    join_room(room_id)

    # Emit welcome message to new player
    # TODO: List other players in the room
    data = {'data': 'Welcome to Shadow Hunters Room: '+room_id, 'color': S_COLOR}
    socketio.emit('message', data, room=request.sid)

@socketio.on('disconnect')
def on_disconnect():

    # Tell everyone in the room about the disconnect
    name = connections[request.sid]['name']
    room_id = connections[request.sid]['room_id']
    socketio.emit('message', {'data': name+' has left the room', 'color': S_COLOR}, room=room_id)

    # FOR DEBUGGING: Print disconnect
    print('{} disconnected from room {}'.format(name, room_id))

    # Remove user from all connection data structures
    connections.pop(request.sid)
    get_sid.pop((name, room_id))

    # Close room if it is now empty
    if len([x for x in connections.values() if x['room_id'] == room_id]) == 0:
        print('everyone left, closing room {}'.format(room_id)) # DEBUGGING
        socketio.close_room(room_id)
        rooms.pop(room_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=80)
