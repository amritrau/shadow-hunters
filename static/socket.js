// Initial connection
var socket = io.connect('http://' + document.domain + ':' + location.port);

$('document').ready(function() {
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
        socket.emit('message', { 'data': user_input });
        $('#message').val('').focus();
    });

    // Start game button
    var start_form = $('#start').on('submit', function(e) {
        e.preventDefault();
        socket.emit('start');
    });

    // Generalized form setup PROTOTYPE (couldnt get it to work)
    /*
    var form_ids = ['confirm', 'yesno', 'select'];
    for (var i = 0; i < form_ids.length; i++)
    {
        $('#'+form_ids[i]).on('submit', function (e) {
            e.preventDefault();
            socket.emit('answer', { 'form': form_ids[i], 'value': $('#'+form_ids[i]+'_fields').val() });
        });
    }
    */
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

// Receive a message and add it to the chat
socket.on('message', function(msg) {
    var html = '<p style="margin:0"><b style="color:'+msg.color+'">';
    if(typeof msg.name !== 'undefined')
    {
        // If there's a user associated with the message, it comes from them
        html += msg.name+'</b> '+msg.data+'</p>';
    }
    else
    {
        // If there's no user associated with the message, it comes from the server
        html += msg.data+'</b></p>';
    }
    $('#message_holder').append(html);
    $("#message_holder").scrollTop($("#message_holder")[0].scrollHeight);
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

socket.on('disconnect', function(reason) {
    console.log("oops i disconnected! reason: "+reason);    
    /*
    if (reason === 'io server disconnect') 
    {
        // the disconnection was initiated by the server, you need to reconnect manually
        socket.connect();
    }
    // else the socket will automatically try to reconnect
    */
});
