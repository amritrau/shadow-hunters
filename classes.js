var GameBoard = new Phaser.Class ({
    Extends: Phaser.Scene,

    initialize:

    function Board ()
    {
        Phaser.Scene.call(this, { key: 'board' });

        this.allowClick = true;

        this.player;

        this.playerTween;
        this.block;
        this.tip;

    },


    preload: function () {
        this.load.image('sky', 'assets/sky.png');
        this.load.image("customTip", "assets/customTip.png");
        this.load.spritesheet('dude',
            'assets/dude.png',
            { frameWidth: 32, frameHeight: 48 }
        );
    },

    create: function () {
        this.add.image(400, 300, 'sky');
        //this.player = this.add.sprite(100, 450, 'dude');
        //this.player.name = "player1";

        this.makePlayer();
        this.block = this.add.image(this.player.x, this.player.y -60, "customTip");
        this.block.setVisible(false);

        this.player.on('clicked', this.clickHandler, this.block);

        this.input.on('gameobjectup', function (pointer, gameObject) {
            gameObject.emit('clicked', gameObject);
        }, this);

        // this.tip = new Phasetips(this, {
        //   targetObject: this.player,
        //   context: "This is a custom tip with custom background, oh yeah!",
        //   position: "top",
        //   positionOffset: 0,
        //   customBackground: this.block,
        //   animation: "grow"
        // });

        //this.time.delayedCall(0, this.startInputEvents, [], this);
    },

    makePlayer: function () {
        var sprite = this.add.sprite(150, 450, 'dude');
        sprite.name = "player1";
        sprite.info = "eek";
        sprite.infobox;
        sprite.setInteractive();
        this.player = sprite;
    },

    clickHandler: function (box)
    {
        if(this.visible == false)
        {
            this.setVisible(true);
        }
        else
        {
            this.setVisible(false);
        }
    },

    startInputEvents: function () {
        this.input.on('gameobjectover', this.onIconOver, this);
        //this.input.on('gameobjectout', this.onIconOut, this);
        //this.input.on('gameobjectdown', this.onIconDown, this);
    },

    stopInputEvents: function () {
        this.input.off('gameobjectover', this.onIconOver);
        //this.input.off('gameobjectout', this.onIconOut);
        //this.input.off('gameobjectdown', this.onIconDown);
    },

    onIconOver: function (pointer, gameObject) {
        var icon = gameObject;
        console.log("hi");
        console.log(icon.name);
        //text.alignTo(icon, Phaser.RIGHT_TOP, 16);
        var style = { font: "32px Courier", fill: "#000000" };
        //sprite.info = this.add.text(0, 0, "Phaser", style);
        var text = this.add.text(0, 0, "lmao", style);
        //Phaser.Display.Align.To.BottomRight(icon.info, icon);
        this.playerTween = this.tweens.add({
            targets: text,
            y: '-=24',
            yoyo: true,
            repeat: 2,
            duration: 300,
            ease: 'Power2'
        });
        //text.destroy();
    },

    removeText: function (text) {
        text.destroy();
    }
});

var config = {
    type: Phaser.CANVAS,
    width: 800,
    height: 600,
    pixelArt: true,
    parent: 'game',
    scene: [ GameBoard ]
};

var game = new Phaser.Game(config);
