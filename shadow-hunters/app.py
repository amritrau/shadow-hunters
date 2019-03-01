from flask import Flask, render_template, url_for, redirect, request, flash
from flask_socketio import SocketIO, join_room, leave_room
from random import randint
from time import sleep
import os

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

# global vars
SOCKET_SLEEP = 0.25
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

# page to join a room
@app.route('/')
def join():
    return render_template('join.html')

# page when you're in the room
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

# GAME STUFF

# gameplay loop
def play(room_id, players):
    players = [Player(user_id, socket_id = get_sid[(user_id, room_id)]) for user_id in players]
    gc = GameContext(
            players = players,
            characters = cli.CHARACTERS,
            black_cards = cli.BLACK_DECK,
            white_cards = cli.WHITE_DECK,
            green_cards = cli.GREEN_DECK,
            areas = cli.AREAS,
            tell_h = lambda x: server_msg(x, room_id),
            direct_h = lambda x, sid: server_msg(x, sid),
            ask_h = lambda x, y, z: ask(x, y, z, room_id),
            update_h = lambda x, y: server_update(x, y, room_id)
        )

    ##### FOR TESTING PURPOSES ONLY ########################
    ##### SEND A DICTIONARY WITH CHARACTER INFO ACROSS #####
    data = str(gc.characters[0].__dict__)
    socketio.emit('game_start', data, room = room_id)
    ##### DELETE THIS WHEN DONE TESTING ####################
    ##### END TESTING PURPOSES ONLY ########################

    winners = gc.play()

# request an action from a specific player in a room
# TODO Consider moving this to separate file
def ask(form, data, player, room_id):
    sid = get_sid[(player, room_id)]
    data['form'] = form
    socketio.emit('ask', data, room=sid)
    while not answer_bins[room_id]['answered']:
        while not answer_bins[room_id]['answered']:
            socketio.sleep(SOCKET_SLEEP)
        # validate answer came from correct person/token blah blah
        # if something is wrong with the answer, mark answered as false again
        if answer_bins[room_id]['sid'] != sid or answer_bins[room_id]['form'] != form:
            answer_bins[room_id]['answered'] = False
    answer_bins[room_id]['answered'] = False
    return answer_bins[room_id]['data']

# send a gameplay update message to all players in a room
# TODO Consider moving this to separate file
def server_msg(data, room_id):
    socketio.emit('message', {'data': data, 'color': 'rgb(37,25,64)'}, room=room_id)
    socketio.sleep(SOCKET_SLEEP)

# TODO Consider moving this to separate file
def server_update(form, data, room_id):
    data['form'] = form
    socketio.emit('update', data, room=room_id)
    socketio.sleep(SOCKET_SLEEP)

# SOCKET STUFF

# join message
@socketio.on('join')
def on_join(json):
    room_id = json['room_id']
    name = json['name']
    get_sid[(name, room_id)] = request.sid
    connections[request.sid] = { 'name': name, 'room_id': room_id }
    connections[request.sid]['color'] = 'rgb('+str(randint(0,150))+','+str(randint(0,150))+','+str(randint(0,150))+')'
    socketio.emit('message', {'data': name+' has joined Shadow Hunters Room: '+room_id, 'color': 'rgb(37,25,64)'}, room=room_id)
    join_room(room_id)
    socketio.emit('message', {'data': 'Welcome to Shadow Hunters Room: '+room_id, 'color': 'rgb(37,25,64)'}, room=request.sid)

# begin play when someone hits 'play'
@socketio.on('start')
def start_game():
    room_id = connections[request.sid]['room_id']
    if rooms[room_id] == 'GAME':
        return
    rooms[room_id] = 'GAME'
    answer_bins[room_id] = {
        'answered': False,
        'sid': '',
        'form': '',
        'data': {}
    }
    players = [x['name'] for x in connections.values() if x['room_id'] == room_id]
    socketio.sleep(SOCKET_SLEEP)
    play(room_id, players)

# receive and validate answer to an ask
@socketio.on('answer')
def receive_answer(json):
    room_id = connections[request.sid]['room_id']
    answer_bins[room_id]['form'] = json.pop('form', None)
    answer_bins[room_id]['data'] = json
    answer_bins[room_id]['sid'] = request.sid
    answer_bins[room_id]['answered'] = True

# post a message to the chat
@socketio.on('post_message')
def message(msg):
    room_id = connections[request.sid]['room_id']
    msg['name'] = connections[request.sid]['name']
    msg['color'] = connections[request.sid]['color']
    socketio.emit('message', msg, room=room_id)

# disconnect message
@socketio.on('disconnect')
def disconnect():
    name = connections[request.sid]['name']
    room_id = connections[request.sid]['room_id']
    socketio.emit('message', {'data': name+' has left the room', 'color': 'rgb(37,25,64)'}, room=room_id)
    connections.pop(request.sid, None)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=80)
