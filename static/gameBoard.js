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
        this.otherPlayers = {};
        this.tip;
        this.gameData;
        this.charInfo;
        this.infoBox;
        this.startSpots = [[490, 220], [530, 220], [570, 220], [510, 260], [550, 260]]; //list of x, y coordinates for 5 players

        // Player location coordinates (row = player number, even columns are x coords, odd columns are y coords)
        this.allSpots = [[336.909,199.411,383.466,117.760,682.109,117.760,728.666,199.411,457.000,342.000,560.000,342.000],
                         [361.909,156.110,408.466, 74.459,657.109, 74.459,703.666,156.110,507.000,342.000,610.000,342.000],
                         [382.965,197.134,429.522,115.483,636.053,115.483,682.610,197.134,482.000,380.747,585.000,380.747],
                         [406.191,239.411,452.748,157.760,612.827,157.760,659.384,239.411,457.000,422.000,560.000,422.000],
                         [431.191,196.110,477.748,114.459,587.827,114.459,634.384,196.110,507.000,422.000,610.000,422.000]
                     ];

        //y coordinates of all possible spots on health bar
        this.hpSpots = [585];
        this.hpStart = 585;
    },

    //function to initialize the data sent into gameboard from waiting room
    init: function (data)
    {
        this.gameData = data;
        this.charInfo = this.gameData.private.character;
        this.allPlayersInfo = this.gameData.public.players;

        /* DEBUGGING
        // console.log(this.charInfo);
        // console.log(typeof this.charInfo);
        // console.log(this.gameData.public);
        // console.log(this.gameData.public.players);
        // var key = Object.keys(this.otherPlayersInfo)[0];
        // console.log(this.otherPlayersInfo[key].user_id);
        // console.log(Object.keys(this.otherPlayersInfo).length);
        // console.log(this.gameData.private);
        */
    },

    //the preload function is where all images that will be used in the game are loaded into
    preload: function () {
        // url where gfx resources are stored
        var gfx = "https://s3.amazonaws.com/shadowhunters.gfxresources/";

        // load background and health bar
        this.load.svg('background', gfx + 'background.svg', {width: 1066, height: 600});
        this.load.image("customTip", "/static/assets/customTip.png");
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

        // load the location cards
        this.load.svg('Hermit\'s Cabin', gfx + 'hermits_cabin.svg', {width: 101, height: 150});
        this.load.svg('Underworld Gate', gfx + 'pleasure_island.svg', {width: 101, height: 150});
        this.load.svg('Church', gfx + 'church.svg', {width: 101, height: 150});
        this.load.svg('Cemetery', gfx + 'cemetery.svg', {width: 101, height: 150});
        this.load.svg('Weird Woods', gfx + 'weird_woods.svg', {width: 101, height: 150});
        this.load.svg('Erstwhile Altar', gfx + 'erstwhile_altar.svg', {width: 101, height: 150});

        // load player sprites and hp trackers
        this.load.svg('player1', gfx + 'white-person.svg', {width: 50.5, height: 37.5});
        this.load.svg('player2', gfx + 'black-person.svg', {width: 50.5, height: 37.5});
        this.load.svg('player3', gfx + 'green-person.svg', {width: 50.5, height: 37.5});
        this.load.svg('player4', gfx + 'blue-person.svg', {width: 50.5, height: 37.5});
        this.load.svg('player5', gfx + 'pink-person.svg', {width: 50.5, height: 37.5});

        this.load.svg('hpp1', gfx + 'whiteDot.svg', {width: 15, height: 15});
        this.load.svg('hpp2', gfx + 'blackDot.svg', {width: 15, height: 15});
        this.load.svg('hpp3', gfx + 'greenDot.svg', {width: 15, height: 15});
        this.load.svg('hpp4', gfx + 'blueDot.svg', {width: 15, height: 15});
        this.load.svg('hpp5', gfx + 'pinkDot.svg', {width: 15, height: 15});

        this.load.image('box', '/static/assets/box.png');

        this.load.svg('charImage', gfx + 'charImage.svg', {width: 123.633, height: 123.633});
        this.load.svg('8hp', gfx + '8hp.svg', {width: 30.14, height: 30.14});
        this.load.svg('12hp', gfx + '12hp.svg', {width: 30.14, height: 30.14});
        this.load.svg('13hp', gfx + '13hp.svg', {width: 30.14, height: 30.14});
        this.load.svg('14hp', gfx + '14hp.svg', {width: 30.14, height: 30.14});
        this.load.svg('A', gfx + 'a.svg', {width: 36.657, height: 36.657});
        this.load.svg('V', gfx + 'v.svg', {width: 36.657, height: 36.657});
        this.load.svg('F', gfx + 'f.svg', {width: 36.657, height: 36.657});
        this.load.svg('G', gfx + 'g.svg', {width: 36.657, height: 36.657});
    },

    //the create function is where everything is added to the canvas
    create: function () {
        var self = this;
        //this adds our background image. the x, y coordinates provided are the center of the canvas
        var background = this.add.image(533, 300, 'background');
        background.setScale(1);
        //background.displayWidth = this.sys.canvas.width;
        //background.displayHeight = this.sys.canvas.height;

        for(var i = 0; i < 15; i++) {
            this.add.image(966, 580 - i*40, String(i));
        }

        // Place locations based on given order
        this.add.image(382.000,201.500, this.gameData.public.zones[0][0].name).setScale(1).angle = -60;
        this.add.image(433.000,113.250, this.gameData.public.zones[0][1].name).setScale(1).angle = -60;
        this.add.image(633.000,113.250, this.gameData.public.zones[1][0].name).setScale(1).angle = 60;
        this.add.image(684.250,201.750, this.gameData.public.zones[1][1].name).setScale(1).angle = 60;
        this.add.image(482.000,382.712, this.gameData.public.zones[2][0].name).setScale(1).angle = 0;
        this.add.image(584.000,382.712, this.gameData.public.zones[2][1].name).setScale(1).angle = 0;


        //this loop creates all players: self and enemies.
        this.nPlayers = Object.keys(this.allPlayersInfo).length;
        var count = 0;
        for(var i = 0; i < this.nPlayers; i++) {
            // console.log("in for loop");
            var key = Object.keys(this.allPlayersInfo)[i];
            if(this.allPlayersInfo[key].user_id === this.gameData.private.user_id) {
                this.player = this.makePlayer(this.allPlayersInfo[key].user_id,
                    this.allPlayersInfo[key], i+1);
                this.player.key = key;
                this.player.on('clicked', this.clickHandler, this.player);
                // console.log(this.player.name);
            }
            else {
                this.otherPlayers[key] = this.makePlayer(this.allPlayersInfo[key].user_id,
                    this.allPlayersInfo[key], i+1);
                this.otherPlayers[key].on('clicked', this.clickHandler, this.otherPlayers[key]);
                count++;
            }
        }

        //this is what makes the box appear when character is clicked. See function clickHandler below
        this.input.on('gameobjectup', function (pointer, gameObject) {
            gameObject.emit('clicked', gameObject);
        }, this);

        //create the information box for the bottom left corner
        this.infoBox = this.add.image(100, 537.5, 'box');

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
            wordWrap: { width: 180, useAdvancedWrap: true }
        });
        var name = this.add.text(5, 460, this.infoBox.data.get('name'), {
            font:'16px Arial' ,
            fill: '#FFFFFF'
        });

        //set the text for inside of the box
        text.setText([
            'Team: ' + this.infoBox.data.get('team'),
            'Win Condition: ' + this.infoBox.data.get('win'), "\n",
            'Special Ability: ' + this.infoBox.data.get('special')
        ]);

        this.add.image(100, 366.975, "charImage");
        this.add.image(60.442, 322.289, this.charInfo.name[0]);
        this.add.image(137.489, 412.722, String(this.charInfo.max_damage) + "hp");

        //align the text inside of our information box
        Phaser.Display.Align.In.TopCenter(name, this.infoBox);
        Phaser.Display.Align.In.TopLeft(text, this.add.zone(110, 560, 200, 130));

        socket.on('update', function(data) {
            self.updateBoard(data);
        });

    },

    makeBox: function() {
        var box  = this.add.box(800, 20, 'text');
        box.name = 'text';
        box.setInteractive();
        this.player = box;
    },

    //the makePlayer function is what creates our sprite and adds him to the board.
    makePlayer: function (name, data, num) {
        var sprite = this.add.sprite(this.startSpots[num-1][0], this.startSpots[num-1][1], 'player' + String(num));
        sprite.hpTracker = this.add.image(900 + (35*(num-1)), this.hpStart, 'hpp' + String(num));

        //our player's name
        sprite.name = name;
        sprite.number = num;

        //this is the information that will appear inside of the info box
        sprite.info = data;
        sprite.spots = {};

        var count = 0;

        for(var i = 0; i < 3; i++) {
            sprite.spots[this.gameData.public.zones[i][0].name] = {x: this.allSpots[num-1][count], y: this.allSpots[num-1][count+1]};
            sprite.spots[this.gameData.public.zones[i][1].name] = {x: this.allSpots[num-1][count+2], y: this.allSpots[num-1][count+3]};
            count += 4;
        }

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
            "Equipment: " + sprite.info.equipment.list
        ]);
        sprite.displayInfo.setVisible(false);

        //this makes the sprite interactive so that we can click on them
        sprite.setInteractive();

        return sprite;
    },

    //updates information about each player
    updatePlayer: function (player, data) {
        if(Object.keys(data.location).length != 0 && player.info.location.name !== data.location.name) {
            player.infoBox.setVisible(false);
            player.displayInfo.setVisible(false);
            player.x = player.spots[data.location.name].x;
            player.y = player.spots[data.location.name].y;
            player.infoBox.x = player.x;
            player.infoBox.y = player.y -60;
            player.displayInfo.x = player.infoBox.x - 120;
            player.displayInfo.y = player.infoBox.y - 40;
            // console.log("sprite moved");
        }

        //TO DO: if hp changes, move token on health bar
        if(player.info.damage != data.damage) {
            player.hpTracker.y = this.hpStart - 40*data.damage;
        }

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
            "Equipment: " + player.info.equipment.list
        ]);
    },

    //for each update, change parts of the board that need to be redrawn.
    updateBoard: function(data) {
        //loop through each player and see if there are things to update
        // console.log(data);
        this.allPlayersInfo = data.players;
        for(var i = 0; i < this.nPlayers; i++){
            var key = Object.keys(this.allPlayersInfo)[i];
            if(key === this.player.key) {
                //update self
                this.updatePlayer(this.player, this.allPlayersInfo[key]);
            }
            else {
                //update other players
                this.updatePlayer(this.otherPlayers[key], this.allPlayersInfo[key]);
            }
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
