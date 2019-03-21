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

    var confirm_form = $('#confirm').on('submit', function(e) {
        e.preventDefault();
        console.log(e);
        socket.emit('answer', { 'form': 'confirm', 'value': $('#confirm [name="inputs"][clicked=true]').val() });
        $('#confirm').hide();
        $('#confirm').empty();
    });

    var yesno_form = $('#yesno').on('submit', function(e) {
        e.preventDefault();
        console.log(e);
        socket.emit('answer', { 'form': 'yesno', 'value': $('#yesno [name="inputs"][clicked=true]').val() });
        $('#yesno').hide();
        $('#yesno').empty();
    });

    var select_form = $('#select').on('submit', function(e) {
        e.preventDefault();
        socket.emit('answer', { 'form': 'select', 'value': $('#select [name="inputs"][clicked=true]').val() });
        $('#select').hide();
        $('#select').empty();
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

// Receive an ask
socket.on('ask', function(data) {
    var option = '';
    if(data.form === 'select') {
        option += '<div id="popup"><br>';
        for (var i = 0; i < data.options.length; i++)
        {
            option += '<button name="inputs" type="submit" class="selectButton" value="'+data.options[i]+'">'+data.options[i]+'</button>';
        }
        option += '<br></div>';
    }
    else {
        for (var i = 0; i < data.options.length; i++)
        {
            option += '<button name="inputs" type="submit" class="button' + String(i+1) + '" value="'+data.options[i]+'">'+data.options[i]+'</button><br>';
        }
    }
    $('#'+data.form).append(option);

    //add click handler to each button
    $('form [name="inputs"]').click(function() {
        $('[name="inputs"]', $(this).parents("form")).removeAttr("clicked");
        $(this).attr("clicked", "true");
    });
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
