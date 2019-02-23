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
answer_bin = {
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
    game_over = False
    while not game_over:
        for player in players:

            # announce player
            server_msg('It\'s '+player+'\'s turn!', room_id)

            # roll for movement
            server_msg(player+' is rolling for movement...', room_id)
            data = {'options': ['Roll for movement!']}
            ask('confirm', data, player, room_id)
            # TODO: GET ACTUAL ROLL FROM DICE
            roll_result = randint(6,7)
            server_update('confirm', {'action': 'roll', 'value': roll_result}, room_id)
            server_msg(player+' rolled a '+str(roll_result)+'!', room_id)

            # select area if a 7 was rolled, else confirm to go to area rolled
            if roll_result == 7:
                server_msg(player+' is selecting an area...', room_id)
                data = {'options': ['Weird Woods', 'Underworld Gate', 'Hermit\'s Cabin', 'Church', 'Cemetery', 'Erstwhile Altar']}
                ask('select', data, player, room_id)
                server_update('select', {'action': 'move', 'value': answer_bin['data']['value']}, room_id)
                server_msg(player+' moves to '+answer_bin['data']['value']+'!', room_id)
            else:
                # TODO: GENERALIZE TO WORK WITH EVERY AREA (NOT JUST CHURCH)
                data = {'options': ['Move to the Church!']}
                ask('confirm', data, player, room_id)
                server_update('confirm', {'action': 'move', 'value': 'Church'}, room_id)
                server_msg(player+' moves to the Church!', room_id)
 
            # yesno to take area action
            data = {'options': ['Perform area action', 'Decline']}
            ask('yesno', data, player, room_id)
            if answer_bin['data']['value'] != 'Decline':
                # TODO: PERFORM AREA ACTION, UPDATE GAME STATE, SEND UPDATE TO CLIENT
                server_update('yesno', {'action': 'area', 'value': 'TODO'}, room_id)
                server_msg(player+' performed their area action!', room_id)
            else:
                server_update('yesno', {}, room_id)
                server_msg(player+' declined to perform their area action.', room_id)
 
            # select target to attack
            server_msg(player+' is picking who to attack...', room_id)
            # TODO: GET ATTACKABLE PLAYERS FROM GAME STATE
            data = {'options': [x for x in players if x != player] + ['Decline']}
            ask('select', data, player, room_id)
            server_update('select', {}, room_id)
           
            # if attacking, roll for damage 
            if answer_bin['data']['value'] != 'Decline':
                target = answer_bin['data']['value']
                server_msg(player+' is attacking '+target+'!', room_id)
                data = {'options': ['Roll for damage!']}
                ask('confirm', data, player, room_id)
                # TODO: GET ACTUAL ROLL FROM DICE
                roll_result = randint(0,5)
                server_update('confirm', {'action': 'roll', 'value': roll_result}, room_id)
                server_msg(player+' rolled a '+str(roll_result)+'!', room_id)
                # TODO: GET ACTUAL DAMAGE DEALT FROM GAME STATE
                damage_dealt = roll_result
                server_update('none', {'action': 'damage', 'player': target, 'value': damage_dealt}, room_id)
                server_msg(player+' hit '+target+' for '+str(damage_dealt)+' damage!', room_id)
            else:
                server_msg(player+' declines to attack.', room_id)

# request an action from a specific player in a room
def ask(form, data, player, room_id):
    sid = get_sid[(player, room_id)]
    data['form'] = form
    socketio.emit('ask', data, room=sid)
    while not answer_bin['answered']:
        while not answer_bin['answered']:
            socketio.sleep(1)
        # validate answer came from correct person/token blah blah
        # if something is wrong with the answer, mark answered as false again 
        if answer_bin['sid'] != sid or answer_bin['form'] != form:
            answer_bin['answered'] = False
    answer_bin['answered'] = False

# send a gameplay update message to all players in a room
def server_msg(data, room_id):
    socketio.emit('message', {'data': data, 'color': s_color}, room=room_id)
    socketio.sleep(1)

def server_update(form, data, room_id):
    data['form'] = form
    socketio.emit('update', data, room=room_id)
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
    socketio.emit('message', {'data': name+' has joined Shadow Hunters Room: '+room_id, 'color': s_color}, room=room_id)
    join_room(room_id)
    socketio.emit('message', {'data': 'Welcome to Shadow Hunters Room: '+room_id, 'color': s_color}, room=request.sid)

# begin play when someone hits 'play'
@socketio.on('start')
def start_game():
    room_id = connections[request.sid]['room_id']
    rooms[room_id] = 'GAME'
    players = [x['name'] for x in connections.values() if x['room_id'] == room_id] 
    # TODO: CREATE GAME CONTEXT AND PERFORM SETUP HERE
    socketio.emit('game_start', {'playerdata': players}, room=room_id)
    socketio.sleep(1)
    play(room_id, players)

# receive and validate answer to an ask
@socketio.on('answer')
def receive_answer(json):
    answer_bin['form'] = json.pop('form', None);
    answer_bin['data'] = json
    answer_bin['sid'] = request.sid
    answer_bin['answered'] = True;

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
    socketio.emit('message', {'data': name+' has left the room', 'color': s_color}, room=room_id)
    connections.pop(request.sid, None)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=80)
