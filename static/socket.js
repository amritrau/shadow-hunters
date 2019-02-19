// EMISSION EVENTS


// Initial connection
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('connect', function() {
    
    // User joins the room
    socket.emit('join', { name: usrctx.name, room_id: usrctx.room_id } );
	
    // Set up message posting with button presses
    var chat_form = $('#chat').on('submit', function(e) {
        e.preventDefault();
        var user_input = $('#message').val();
        socket.emit('post_message', { 'contents': user_input });
        $('#message').val('').focus();
    });

    // Start game button
    var start_form = $('#start').on('submit', function(e) {
        e.preventDefault();
        socket.emit('start');
    });

    // In-game form response setup
    var roll_form = $('#roll').on('submit', function(e) {
        e.preventDefault();
        socket.emit('answer', { 'value': '5' });
        $('#roll').hide();
        $('#wait').show();
    });

    var attack_form = $('#attack').on('submit', function(e) {
        e.preventDefault();
        var user_input = $('#target').val();
        socket.emit('answer', { 'value': user_input });
        $('#target').val('').focus();
        $('#attack').hide();
        $('#wait').show();
    });

    var move_form = $('#move').on('submit', function(e) {
        e.preventDefault();
        var user_input = $('#area').val();
        socket.emit('answer', { 'value': user_input });
        $('#area').val('').focus();
        $('#move').hide();
        $('#wait').show();
    });

    $('#roll').hide();
    $('#attack').hide();
    $('#move').hide();

});


// RECEPTION EVENTS


// Receive a message and add it to the chat
socket.on('message', function(msg) {
    var html = '<p style="margin:0"><b style="color:'+msg.color+'">';
    if(typeof msg.name !== 'undefined')
    {
        // If there's a user associated with the message, it comes from them
        html += msg.name+'</b> '+msg.contents+'</p>';
    }
    else
    {
        // If there's no user associated with the message, it comes from the server
        html += msg.contents+'</b></p>';
    }
    $('#message_holder').append(html);
    $("#message_holder").scrollTop($("#message_holder")[0].scrollHeight);
});

// Receive the signal to start the game
socket.on('game_start', function(game_data) {
    $('#start').remove();
    // SET UP GAME INTERFACE BASED ON GAME_DATA HERE
    var html = '<p id="wait">Waiting...</p>';
    $('#game').append(html);
});

// Receive an ask
socket.on('ask', function(ask_data) {
    $('#wait').hide();
    $('#'+ask_data.type).show();
});
