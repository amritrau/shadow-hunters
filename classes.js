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
        this.load.image('0', 'assets/zero.png');
        this.load.image('1', 'assets/one.png');
        this.load.image('2', 'assets/two.png');
        this.load.image('3', 'assets/three.png');
        this.load.image('4', 'assets/four.png');
        this.load.image('5', 'assets/five.png');
        this.load.image('6', 'assets/six.png');
        this.load.image('7', 'assets/seven.png');
        this.load.image('8', 'assets/eight.png');
        this.load.image('9', 'assets/nine.png');
        this.load.image('10', 'assets/ten.png');
        this.load.image('11', 'assets/eleven.png');
        this.load.image('12', 'assets/twelve.png');
        this.load.image('13', 'assets/thirteen.png');
        this.load.image('14', 'assets/fourteen.png');
        this.load.image('text', 'assets/text.png');



    },

    create: function () {
        this.add.image(400, 300, 'sky');
        this.add.image(700,20, '14');
        this.add.image(700,60, '13');
        this.add.image(700,100, '12');
        this.add.image(700,140, '11');
        this.add.image(700,180, '10');
        this.add.image(700,220, '9');
        this.add.image(700,260, '8');
        this.add.image(700,300, '7');
        this.add.image(700,340, '6');
        this.add.image(700,380, '5');
        this.add.image(700,420, '4');
        this.add.image(700,460, '3');
        this.add.image(700,500, '2');
        this.add.image(700,540, '1');
        this.add.image(700,580, '0');


        //this.player = this.add.sprite(100, 450, 'dude');
        //this.player.name = "player1";

        this.makeBox();
        this.block = this.add.image(this.player.x +20, this.player.y, "text");
        this.block.setVisible(false);
        this.player.on('clicked', this.clickHandler, this.block);

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

    makeBox: function() {
        var box  = this.add.box(800, 20, 'text');
        box.name = 'text';
        box.setInteractive();
        this.player = box;
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
