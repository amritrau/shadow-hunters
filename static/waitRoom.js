// this is the scene that will be used in the waiting room, i.e. before the game starts
var WaitingRoom = new Phaser.Class ({
    Extends: Phaser.Scene,

    initialize:

    function Room () {
        Phaser.Scene.call(this, {key: 'menu'});
    },

    preload: function () {
        // Send right to board if spectating
        if(usrctx.spectate) return;

        // url where gfx resources are stored
        var gfx = "https://s3.amazonaws.com/shadowhunters.gfxresources/";
        this.load.svg('background', gfx + 'background.svg', {width: 1066, height: 600});
    },

    create: function () {
        // Send right to board if spectating
        var self = this;
        if(usrctx.spectate)
        {
            // Start board
            self.scene.start('board', usrctx.gc_data);
            return;
        }

        //this resizes the background image to fit into our canvas
        var background = this.add.image(533, 300, 'background');
        background.setScale(1);
        //background.displayWidth = this.sys.canvas.width;
        //background.displayHeight = this.sys.canvas.height;

        //SOCKET CALL! if game start button pressed, then we switch scenes and go to the game board
        socket.on("game_start", function (data) {
            $('#start').remove();
            console.log(data);
            self.scene.start('board', data);
        });
    }
});
