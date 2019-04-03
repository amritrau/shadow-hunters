// Don't do anything until the DOM loads
// First, establish socket connection and set up handlers
// Then, set up and start game
$('document').ready(function() {

    // Forms are initially hidden
    $('#confirm').hide();
    $('#yesno').hide();
    $('#select').hide();
    $('#reveal').hide();
    if(usrctx.spectate) $('#start').remove();

    // Initial connection
    socket = io.connect('http://' + document.domain + ':' + location.port, {reconnection: false});
    socket.on('connect', function() {

        // User joins the room
        socket.emit('join', { name: usrctx.name, room_id: usrctx.room_id, spectate: usrctx.spectate } );

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

        // Reveal button
        var reveal_form = $('#reveal').on('submit', function(e) {
            e.preventDefault();
            socket.emit('reveal');
        });

        // Form type 1
        var confirm_form = $('#confirm').on('submit', function(e) {
            e.preventDefault();
            console.log(e);
            socket.emit('answer', { 'form': 'confirm', 'value': $('#confirm [name="inputs"][clicked=true]').val() });
            $('#confirm').hide();
            $('#confirm').empty();
        });

        // Form type 2
        var yesno_form = $('#yesno').on('submit', function(e) {
            e.preventDefault();
            console.log(e);
            socket.emit('answer', { 'form': 'yesno', 'value': $('#yesno [name="inputs"][clicked=true]').val() });
            $('#yesno').hide();
            $('#yesno').empty();
        });

        // Form type 3
        var select_form = $('#select').on('submit', function(e) {
            e.preventDefault();
            socket.emit('answer', { 'form': 'select', 'value': $('#select [name="inputs"][clicked=true]').val() });
            $('#select').hide();
            $('#select').empty();
        });

        // Receive a message
        socket.on('message', function(msg) {

            // Build message
            var html = '<p style="margin:0"><b style="color:'+msg.color+'">';
            if(typeof msg.name !== 'undefined')
            {
                html += msg.name+'</b> '+msg.data+'</p>';
            }
            else
            {
                html += msg.data+'</b></p>';
            }

            // Put message in chatbox
            $('#message_holder').append(html);
            $("#message_holder").scrollTop($("#message_holder")[0].scrollHeight);
        });

        // Receive an ask
        socket.on('ask', function(data) {

            // Add buttons for each option
            var option = '';
            if(data.form === 'select')
            {
                option += '<div id="popup"><br>';
                for (var i = 0; i < data.options.length; i++)
                {
                    option += '<button name="inputs" type="submit" class="selectButton" value="' +
                    data.options[i] + '">' + data.options[i] + '</button>';
                }
                option += '<br></div>';
            }
            else
            {
                for (var i = 0; i < data.options.length; i++)
                {
                    option += '<button name="inputs" type="submit" class="button' +
                               String(i+1) + '" value="' + data.options[i] + '">' +
                               data.options[i] + '</button><br>';
                }
            }
            $('#'+data.form).append(option);

            // add click handler to each button
            $('form [name="inputs"]').click(function() {
                $('[name="inputs"]', $(this).parents("form")).removeAttr("clicked");
                $(this).attr("clicked", "true");
            });

            // Show buttons
            $('#'+data.form).show();
        });

        // Disconnect handler
        socket.on('disconnect', function(reason) {
            window.location = "/";
        });

        // Configure game
        var config = {
            type: Phaser.CANVAS,
            width: 1066,
            height: 600,
            pixelArt: false,
            parent: 'board',
            scene: [ WaitingRoom, GameBoard ]
        };

        // Start up waiting room and phaser game
        var game = new Phaser.Game(config);
    });
});
