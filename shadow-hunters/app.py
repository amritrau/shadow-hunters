from flask import Flask, render_template, url_for, redirect, request
from flask_socketio import SocketIO, join_room, leave_room
from random import randint
from time import sleep
import os

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
connections = {}
rooms = {}
get_sid = {}

s_color = 'rgb(37,25,64)'
answered = False
answer_bin = {}


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
        username = ''
        room_id = ''
        try:
            username = request.form.get('username')
            room_id = request.form.get('room_id')
        except:
            return redirect('/')

        # don't let someone in if there's a game in progress in the room
        if room_id in rooms and rooms[room_id] == 'GAME':
            return redirect('/')
        else:
            rooms[room_id] = 'LOBBY'

        # send them to join the room!
        return render_template('room.html', context={ 'name': username, 'room_id': room_id })
    else:
        return redirect('/')


# GAME STUFF


# gameplay loop
def play(room_id, players):
    for player in players:

        # announce the turn
        server_msg('It\'s '+player+'\'s turn!', room_id)

        # options about the ask (i.e. if the ask is to choose a player, 
        # should have which players you can pick). example below.
        # these should be set before every ask, based on the current
        # game state.
        options = {'PLAYER': ['gia', 'joanna', 'vishal'],
                   'AREA': ['WEIRD WOODS', 'pleasure island']}

        # example of intelligence
        options['PLAYER'].remove(player)

        # simple garbage game loop

        # roll for movement
        server_msg(player+' is rolling...', room_id)
        ask(player, room_id, "roll", options)
        server_msg(player+' rolled a '+answer_bin['value']+'!', room_id)

        # pick an area even though you don't actually do this
        server_msg(player+' is selecting an area...', room_id)
        ask(player, room_id, "move", options)
        server_msg(player+' moves to '+answer_bin['value']+'!', room_id)
        
        # attack someone!
        server_msg(player+' is picking who to attack...', room_id)
        ask(player, room_id, "attack", options)
        server_msg(player+' attacks '+answer_bin['value']+'!', room_id)

# request an action from a specific player in a room
def ask(player, room_id, ask_type, options):
    global answered, answer_bin
    sid = get_sid[(player, room_id)]
    options['type'] = ask_type
    socketio.emit('ask', options, room=sid)
    while not answered:
        while not answered:
            socketio.sleep(1)
        # validate answer came from correct person/token blah blah
        # if something is wrong with the answer, mark answered as false again 
        if answer_bin['sid'] != sid:
            answered = False
    answered = False

# send a gameplay update message to all players in a room
def server_msg(contents, room_id):
    socketio.emit('message', {'contents': contents, 'color': s_color}, room=room_id)
    socketio.sleep(1)

    
# SOCKET STUFF


# join message
@socketio.on('join')
def on_join(json):
    room_id = json['room_id']
    name = json['name']
    get_sid[(name, room_id)] = request.sid
    connections[request.sid] = { 'name': name, 'room_id': room_id }
    connections[request.sid]['color'] = 'rgb('+str(randint(0,150))+','+str(randint(0,150))+','+str(randint(0,150))+')'
    socketio.emit('message', {'contents': name+' has joined Shadow Hunters Room: '+room_id, 'color': s_color}, room=room_id)
    join_room(room_id)
    socketio.emit('message', {'contents': 'Welcome to Shadow Hunters Room: '+room_id, 'color': s_color}, room=request.sid)

# begin play when someone hits 'play'
@socketio.on('start')
def start_game():
    room_id = connections[request.sid]['room_id']
    rooms[room_id] = 'GAME'
    players = [x['name'] for x in connections.values() if x['room_id'] == room_id] 
    # CREATE GAME CONTEXT AND PERFORM SETUP HERE
    socketio.emit('game_start', {'playerdata': players}, room=room_id)
    socketio.sleep(1)
    play(room_id, players)

# receive and validate answer to an ask
@socketio.on('answer')
def receive_answer(json):
    global answered, answer_bin
    answer_bin = json
    answer_bin['sid'] = request.sid
    answered = True;

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
    socketio.emit('message', {'contents': name+' has left the room', 'color': s_color}, room=room_id)
    connections.pop(request.sid, None)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=80)
