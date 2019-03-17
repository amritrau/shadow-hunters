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
