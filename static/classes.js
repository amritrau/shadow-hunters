// url where gfx resources are stored
var gfx = "https://s3.amazonaws.com/shadowhunters.gfxresources/"

// this is the scene that will be used in the waiting room, i.e. before the game starts
var WaitingRoom = new Phaser.Class ({
    Extends: Phaser.Scene,

    initialize:

    function Room () {
        Phaser.Scene.call(this, {key: 'menu'});
    },
    preload: function () {
        this.load.image('background', gfx + 'background-1066.png');
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
        this.startSpots = [490, 220, 530, 220, 570, 220, 510, 260, 550, 260]; //list of x, y coordinates for 5 players
        this.allSpots = [];
    },

    //function to initialize the data sent into gameboard from waiting room
    init: function (data)
    {
        this.gameData = data;
        this.charInfo = this.gameData.private.character;
        this.allPlayersInfo = this.gameData.public.players;

        //BELOW CODE FOR DEBUGGING - uncomment to use
        // console.log(this.charInfo);
        // console.log(typeof this.charInfo);
        //console.log(this.gameData.public);
        // console.log(this.gameData.public.players);
        // var key = Object.keys(this.otherPlayersInfo)[0];
        // console.log(this.otherPlayersInfo[key].user_id);
        // console.log(Object.keys(this.otherPlayersInfo).length);
        // console.log(this.gameData.private);
    },

    //the preload function is where all images that will be used in the game are loaded into
    preload: function () {
        this.load.image('background', gfx + 'background-1066.png');
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
            //console.log("in for loop");
            var key = Object.keys(this.allPlayersInfo)[i];
            if(this.allPlayersInfo[key].user_id === this.gameData.private.user_id) {
                this.player = this.makePlayer(this.allPlayersInfo[key].user_id,
                    this.allPlayersInfo[key], this.startSpots[2*i], this.startSpots[2*i+1]);
                this.player.key = key;
                this.player.on('clicked', this.clickHandler, this.player);
                //console.log(this.player.name);
            }
            else {
                this.otherPlayers[count] = this.makePlayer(this.allPlayersInfo[key].user_id,
                    this.allPlayersInfo[key], this.startSpots[2*i], this.startSpots[2*i+1]);
                this.otherPlayers[count].key = key;
                this.otherPlayers[count].on('clicked', this.clickHandler, this.otherPlayers[count]);
                count++;
            }
        }

        //this is what makes the box appear when character is clicked. See function clickHandler below
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
        var text = this.add.text(10, 470, '', {
            font: '12px Arial',
            fill: '#FFFFFF',
            wordWrap: { width: 150, useAdvancedWrap: true }
        });
        var name = this.add.text(5, 460, this.infoBox.data.get('name'), {
            font:'16px Arial' ,
            fill: '#FFFFFF'
        });

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
            //possible issue: getting too many updates
            self.updateBoard(data);
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
        sprite.spots = {};

        for(var i = 0; i < 3; i++) {
            sprite.spots[this.gameData.public.zones[i][0].name] = {x: locx - 200 + 140*(i*i), y: locy + 110*(i%2)};
            sprite.spots[this.gameData.public.zones[i][1].name] = {x: locx - 100 + 140*(i*i), y: locy - 120 + 230*(i%2)};
        }

        console.log(sprite.spots);

        if(Object.keys(sprite.info.location).length == 0) {
            sprite.info.location.name = "None";
        }

        if(Object.keys(sprite.info.equipment).length == 0) {
            sprite.info.equipment.list = "None";
        }

        //this creates the infobox, i.e. the box that will appear when we click on him.
        sprite.infoBox = this.add.image(sprite.x, sprite.y -60, "customTip");
        sprite.infoBox.setVisible(false);
        sprite.displayInfo = this.add.text(sprite.infoBox.x - 120, sprite.infoBox.y - 40, " ", { font: '12px Arial', fill: '#FFFFFF', wordWrap: { width: 250, useAdvancedWrap: true }});
        sprite.displayInfo.setText([
            "Player: " + sprite.name,
            "Equipment: " + sprite.info.equipment.list,
            "Current Damage: " + sprite.info.hp,
            "Location: " + sprite.info.location.name
        ]);
        sprite.displayInfo.setVisible(false);

        //this makes the sprite interactive so that we can click on him
        sprite.setInteractive();

        return sprite;
    },

    //updates information about each player
    updatePlayer: function (player, data) {
        //TO DO: if location is different, move character
        if(Object.keys(data.location).length != 0 && player.info.location.name !== data.location.name) {
            // console.log(player.x);
            // console.log(data);
            // console.log(player.spots[data.location.name]);
            player.x = player.spots[data.location.name].x;
            player.y = player.spots[data.location.name].y;
            // player.infoBox.x = player.x;
            // player.infoBox.y = player.y -60;
            // player.displayInfo.x = player.infoBox.x - 120;
            // player.displayInfo.y = player.infoBox.y - 40;
            console.log("sprite moved");
        }
        //TO DO: if hp changes, move token on health bar
        player.info = data;
        if(Object.keys(player.info.location).length == 0) {
            player.info.location.name = "None";
        }

        var nEquip = Object.keys(player.info.equipment).length;
        if(nEquip == 0) {
            player.info.equipment.list = "None";
        }
        else {
            player.info.equipment.list = "";
            for(var i = 0; i < nEquip; i++) {
                player.info.equipment.list += player.info.equipment[i].title;
                if(i < nEquip-1){
                    player.info.equipment.list += ", ";
                }
            }
        }
        player.displayInfo.setText([
            "Player: " + player.name,
            "Equipment: " + player.info.equipment.list,
            "Current Damage: " + player.info.hp,
            "Location: " + player.info.location.name
        ]);
    },

    //for each update, change parts of the board that need to be redrawn.
    updateBoard: function(data) {
        //loop through each player and see if there are things to update
        //console.log(data);
        this.allPlayersInfo = data.players;
        var count = 0;
        for(var i = 0; i < this.nPlayers; i++){
            var key = Object.keys(this.allPlayersInfo)[i];
            if(key === this.player.key) {
                //update self
                this.updatePlayer(this.player, this.allPlayersInfo[key]);
            }
            else {
                //update other players
                this.updatePlayer(this.otherPlayers[count], this.allPlayersInfo[key]);
                count++;
            }
        }

    },
    //if player clicked and box is visible, make invisible. if box is invisible, make visible
    clickHandler: function (player)
    {
        if(this.infoBox.visible == false)
        {
            //Move infoBox. I put this here for layering purposes; when its
            //in updatePlayer, for some reason, other sprites appear on top of the box.
            this.infoBox.x = this.x;
            this.infoBox.y = this.y -60;
            this.displayInfo.x = this.infoBox.x - 120;
            this.displayInfo.y = this.infoBox.y - 40;
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
    pixelArt: false,
    parent: 'board',
    scene: [ WaitingRoom, GameBoard ]
};

//this starts the game
var game = new Phaser.Game(config);
