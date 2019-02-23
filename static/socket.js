// EMISSION EVENTS


// Initial connection
var socket = io.connect('http://' + document.domain + ':' + location.port);

$('document').ready(function(){
    $('#confirm').hide();
    $('#yesno').hide();
    $('#select').hide();
});

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
    var confirm_form = $('#confirm').on('submit', function(e) {
        e.preventDefault();
        socket.emit('answer', { 'form': 'confirm', 'value': $('#confirm_fields').val() });
    });

    var yesno_form = $('#yesno').on('submit', function(e) {
        e.preventDefault();
        socket.emit('answer', { 'form': 'yesno', 'value': $('#yesno_fields').val() });
    });

    var select_form = $('#select').on('submit', function(e) {
        e.preventDefault();
        socket.emit('answer', { 'form': 'select', 'value': $('#select_fields').val() });
    });
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
socket.on('game_start', function(data) {
    $('#start').remove();
    // TODO: SET UP INITIAL UI BASED ON GAME_DATA HERE
    var html = '<p id="wait">Waiting...</p>';
    $('#game').append(html);
});

// Receive a game state update
socket.on('update', function(data) {
    $('#'+data.form).hide();
    $('#'+data.form+'_fields').empty();
    // TODO: UPDATE UI TO REFLECT UPDATE
    $('#wait').show();
});

// Receive an ask
socket.on('ask', function(data) {
    $('#wait').hide();
    var option = '';
    for (var i = 0; i < data.options.length; i++) 
    {
        option += '<option value="'+data.options[i]+'">'+data.options[i]+'</option>';
    }
    $('#'+data.form+'_fields').append(option);
    $('#'+data.form).show();
});
