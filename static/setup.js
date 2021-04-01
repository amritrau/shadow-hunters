// Don't do anything until the DOM loads
// First, establish socket connection and set up handlers
// Then, set up and start game
$('document').ready(function() {

    // Forms are initially hidden
    $('#confirm').hide();
    $('#yesno').hide();
    $('#select').hide();
    $('#reveal').hide();
    $('#special').hide();
    if(usrctx.spectate) {
        $('#start').remove();
        $('#reveal').remove();
        $('#special').remove();
    }

    // Initial connection
    socket = io.connect('http://' + document.domain + ':' + location.port, {
        reconnection: false,
        'sync disconnect on unload': true
    });
    socket.on('connect', async function() {

        // Receive a message
        socket.on('message', function(msg) {

            // Build message
            var html = '';
            if(typeof msg.name !== 'undefined') {
                html = '<p style="margin:0"><b style="color:'+msg.color+'">'+msg.name+'</b> '+msg.data+'</p>';
            }
            else {
                html = '<p style="margin:0">';
                for(var i = 0; i < msg.strings.length; i++) {
                    html += '<b style="color:'+msg.colors[i]+'">'+msg.strings[i]+'</b>';
                }
                html += '</p>';
            }

            // Put message in chatbox and snap to bottom if already at bottom
            var chat = $("#message_holder");
            if (chat.scrollTop() == chat[0].scrollHeight - chat[0].clientHeight) {
                chat.append(html);
                chat.scrollTop(chat[0].scrollHeight);
            }
            else {
                chat.append(html);
            }
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

            // Add click handler to each button
            $('form [name="inputs"]').click(function() {
                $('[name="inputs"]', $(this).parents("form")).removeAttr("clicked");
                $(this).attr("clicked", "true");
            });

            // Show buttons
            $('#'+data.form).show();
        });

        // False start handler
        socket.on('false_start', function(data) {
            alert("You cannot start a "+data.field+"-player game when there are "+data.actual+" people in the room.");
        });

        // Disconnect handler
        socket.on('disconnect', function(reason) {
            window.onbeforeunload = function() {};
            alert("You have lost connection to the server – click 'Ok' to return to the home page, " +
                  "where you may reconnect if you were in a game.");
            window.location = "/";
        });

        // Close window handler
        window.onbeforeunload = function() {
            socket.close();
        }

        // User joins the room
        socket.emit('join', usrctx );

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
            socket.emit('start', { 'n_players': $('#nPlayers').val() });
        });

        // Reveal button
        var reveal_form = $('#reveal').on('submit', function(e) {
            e.preventDefault();
            $('#reveal').hide();
            socket.emit('reveal');
        });

        // Special ability button
        var special_form = $('#special').on('submit', function(e) {
            e.preventDefault();
            $('#special').hide();
            socket.emit('special');
        });

        // Form type 1
        var confirm_form = $('#confirm').on('submit', function(e) {
            e.preventDefault();
            socket.emit('answer', { 'value': $('#confirm [name="inputs"][clicked=true]').val() });
            $('#confirm').hide();
            $('#confirm').empty();
        });

        // Form type 2
        var yesno_form = $('#yesno').on('submit', function(e) {
            e.preventDefault();
            socket.emit('answer', { 'value': $('#yesno [name="inputs"][clicked=true]').val() });
            $('#yesno').hide();
            $('#yesno').empty();
        });

        // Form type 3
        var select_form = $('#select').on('submit', function(e) {
            e.preventDefault();
            socket.emit('answer', { 'value': $('#select [name="inputs"][clicked=true]').val() });
            $('#select').hide();
            $('#select').empty();
        });

        // Configure game
        var config = {
            type: Phaser.AUTO,
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
