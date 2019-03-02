// this is the scene that will be used in the waiting room, i.e. before the game starts
var WaitingRoom = new Phaser.Class ({
    Extends: Phaser.Scene,

    initialize:

    function Room () {
        Phaser.Scene.call(this, {key: 'menu'});
    },
    preload: function () {
        this.load.image('background', '/static/assets/background.jpg');
    },

    create: function () {
        var self = this;

        //this resizes the background image to fit into our canvas
        var background = this.add.image(533, 300, 'background');
        background.displayWidth = this.sys.canvas.width;
        background.displayHeight = this.sys.canvas.height;

        //SOCKET CALL! if game start button pressed, then we switch scenes and go to the game board
        socket.on("game_start", function (data) {
            $('#start').remove();
            var html = '<p id="wait">Waiting...</p>';
            $('#game').append(html);
            self.scene.start('board', data);
        });
    }
});

//gameboard scene: this is the actual canvas for the game!
var GameBoard = new Phaser.Class ({
    Extends: Phaser.Scene,

    initialize:

    function Board () {
        // this names the scene we are in
        Phaser.Scene.call(this, { key: 'board' });

        // this allows clicking in our game
        this.allowClick = true;

        //this is where all of the objects specific to our scene will appear
        this.player;
        this.allPlayersInfo;
        this.nPlayers;
        this.otherPlayers = [];
        this.tip;
        this.gameData;
        this.charInfo;
        this.infoBox;

    },

    //function to initialize the data sent into gameboard from waiting room
    init: function (data)
    {
        this.gameData = data;
        this.charInfo = this.gameData.private.character;
        this.allPlayersInfo = this.gameData.public.players;
        // console.log(this.charInfo);
        // console.log(typeof this.charInfo);
        // console.log(this.gameData.public);
        // console.log(this.gameData.public.players);
        // var key = Object.keys(this.otherPlayersInfo)[0];
        // console.log(this.otherPlayersInfo[key].user_id);
        // console.log(Object.keys(this.otherPlayersInfo).length);
        // console.log(this.gameData.private);
    },

    //the preload function is where all images that will be used in the game are loaded into
    preload: function () {
        this.load.image('background', '/static/assets/background.jpg');
        this.load.image("customTip", "/static/assets/customTip.png");
        this.load.spritesheet('dude',
            '/static/assets/dude.png',
            { frameWidth: 32, frameHeight: 48 }
        );
        this.load.image('0', '/static/assets/zero.png');
        this.load.image('1', '/static/assets/one.png');
        this.load.image('2', '/static/assets/two.png');
        this.load.image('3', '/static/assets/three.png');
        this.load.image('4', '/static/assets/four.png');
        this.load.image('5', '/static/assets/five.png');
        this.load.image('6', '/static/assets/six.png');
        this.load.image('7', '/static/assets/seven.png');
        this.load.image('8', '/static/assets/eight.png');
        this.load.image('9', '/static/assets/nine.png');
        this.load.image('10', '/static/assets/ten.png');
        this.load.image('11', '/static/assets/eleven.png');
        this.load.image('12', '/static/assets/twelve.png');
        this.load.image('13', '/static/assets/thirteen.png');
        this.load.image('14', '/static/assets/fourteen.png');
        this.load.image('text', '/static/assets/text.png');




        this.load.image('box', '/static/assets/box.png');
    },

    //the create function is where everything is added to the canvas
    create: function () {
        var self = this;
        //this adds our background image. the x, y coordinates provided are the center of the canvas
        var background = this.add.image(533, 300, 'background');
        background.displayWidth = this.sys.canvas.width;
        background.displayHeight = this.sys.canvas.height;

        this.add.image(970,20, '14');
        this.add.image(970,60, '13');
        this.add.image(970,100, '12');
        this.add.image(970,140, '11');
        this.add.image(970,180, '10');
        this.add.image(970,220, '9');
        this.add.image(970,260, '8');
        this.add.image(970,300, '7');
        this.add.image(970,340, '6');
        this.add.image(970,380, '5');
        this.add.image(970,420, '4');
        this.add.image(970,460, '3');
        this.add.image(970,500, '2');
        this.add.image(970,540, '1');
        this.add.image(970,580, '0');

        //this.makeBox();
       // this.block = this.add.image(this.player.x +20, this.player.y, "text");
       // this.block.setVisible(false);
       // this.player.on('clicked', this.clickHandler, this.block);

       //this loop creates all players: self and enemies.
        this.nPlayers = Object.keys(this.allPlayersInfo).length;
        var count = 0;
        for(var i = 0; i < this.nPlayers; i++) {
            console.log("in for loop");
            var key = Object.keys(this.allPlayersInfo)[i];
            console.log(this.allPlayersInfo[key].user_id);
            console.log(this.gameData.private.user_id);
            if(this.allPlayersInfo[key].user_id === this.gameData.private.user_id) {
                this.player = this.makePlayer(this.allPlayersInfo[key].user_id, this.allPlayersInfo[key], 300 + 20*i, 400);
                this.player.on('clicked', this.clickHandler, this.player);
                console.log(this.player.name);
            }
            else {
                this.otherPlayers[count] = this.makePlayer(this.allPlayersInfo[key].user_id, this.allPlayersInfo[key], 300 + 20*i, 400);
                this.otherPlayers[count].on('clicked', this.clickHandler, this.otherPlayers[i-1]);
                count++;
            }
            //this.otherPlayers[i] = this.add.sprite(this.player.x + 10*i, this.player.y, "dude");
        }

        //this is what makes the box appear when character is clocked. See function clickHandler below
        this.input.on('gameobjectup', function (pointer, gameObject) {
            gameObject.emit('clicked', gameObject);
        }, this);

        //create the information box for the bottom left corner
        this.infoBox = this.add.image(75, 525, 'box');

        //amrit sets character allegance to a number. we convert it to a team
        if(this.charInfo.alleg == 1){
            this.charInfo.alleg = "Neutral";
        }
        else if (this.charInfo.alleg == 0) {
            this.charInfo.alleg = "Shadow";
        }
        else {
            this.charInfo.alleg = "Hunter";
        }
        //enable data to be stored in this box. I'm not sure if this is necessary; if it isn't we can delete these set lines below
        this.infoBox.setDataEnabled();
        this.infoBox.data.set("name", this.charInfo.name);
        this.infoBox.data.set("team", this.charInfo.alleg);
        this.infoBox.data.set("win", this.charInfo.win_cond_desc);
	this.infoBox.data.set("special", "none"); //not yet implemented

        //create the text variables
        var text = this.add.text(10, 470, '', { font: '12px Arial', fill: '#FFFFFF', wordWrap: { width: 150, useAdvancedWrap: true }});
        var name = this.add.text(5, 460, this.infoBox.data.get('name'), { font:'16px Arial' ,fill: '#FFFFFF'});

        //set the text for inside of the box
        text.setText([
            'Team: ' + this.infoBox.data.get('team'),
            'Win Condition: ' + this.infoBox.data.get('win') + '\n',
            'Special Ability: ' + this.infoBox.data.get('special')
        ]);

        //align the text inside of our information box
        Phaser.Display.Align.In.TopCenter(name, this.infoBox);
        Phaser.Display.Align.In.TopLeft(text, this.add.zone(70, 545, 130, 130));

        socket.on('update', function(data) {
            $('#'+data.form).hide();
            $('#'+data.form+'_fields').empty();
            // TODO: UPDATE UI TO REFLECT UPDATE
            if(data.action === "move") {
                console.log(data);
                if(data.player === self.player.name) {
                    self.updatePlayer(self.player, data.action, data.value);
                }
                else{
                    for(var i = 0; i < self.nPlayers - 1; i++){
                        if(data.player === self.otherPlayers[i].name) {
                            self.updatePlayer(self.otherPlayers[i], data.action, data.value);
                            break;
                        }
                    }
                }
            }
            $('#wait').show();
        });

    },

    makeBox: function() {
        var box  = this.add.box(800, 20, 'text');
        box.name = 'text';
        box.setInteractive();
        this.player = box;
    },


    //the makePlayer function is what creates our sprite and adds him to the board.
    makePlayer: function (name, data, locx, locy) {
        var sprite = this.add.sprite(locx, locy, 'dude');

        //our player's name
        sprite.name = name;

        //this is the information that will appear inside of the info box
        sprite.info = data;

        //this creates the infobox, i.e. the box that will appear when we click on him.
        sprite.infoBox = this.add.image(sprite.x, sprite.y -60, "customTip");
        sprite.infoBox.setVisible(false);
        sprite.displayInfo = this.add.text(sprite.infoBox.x - 120, sprite.infoBox.y - 40, " ", { font: '12px Arial', fill: '#FFFFFF', wordWrap: { width: 150, useAdvancedWrap: true }});
        sprite.displayInfo.setText([
            "Player: " + sprite.name,
            "Equipment: " + sprite.info.equipment,
            "Current Damage: " + sprite.info.hp,
            "Location: " + sprite.info.location
        ]);
        sprite.displayInfo.setVisible(false);

        //this makes the sprite interactive so that we can click on him
        sprite.setInteractive();

        return sprite;
    },

    //updates information about each player
    updatePlayer: function (player, action_type, change) {
        if(action_type === "move") {
            player.info.location = change;
            console.log("in updatePlayer function: action type is move");
            console.log("in updatePlayer: location is ", change);
            player.displayInfo.setText([
                "Player: " + player.name,
                "Equipment: " + player.info.equipment,
                "Current Damage: " + player.info.hp,
                "Location: " + player.info.location
            ]);
        }
    },

    //if player clicked and box is visible, make invisible. if box is invisible, make visible
    clickHandler: function (player)
    {
        if(this.infoBox.visible == false)
        {
            this.infoBox.setVisible(true);
            this.displayInfo.setVisible(true);
        }
        else
        {
            this.infoBox.setVisible(false);
            this.displayInfo.setVisible(false);
        }
    }
});

//create game configurations
var config = {
    type: Phaser.CANVAS,
    width: 1066,
    height: 600,
    pixelArt: true,
    parent: 'board',
    scene: [ WaitingRoom, GameBoard ]
};

//this starts the game
var game = new Phaser.Game(config);
