import { Selector } from 'testcafe';

fixture `Integration`
    .page `localhost:5000`;

const screen_name = 'amritrau'
const room_id = 'akw200'


test('Join room', async t => {
    await t
        .typeText('#screen-name', screen_name)
        .typeText('#room-id', room_id)
        .click('#submit-button');

    const location = await t.eval(() => window.location);
    await t.expect(location.pathname).eql('/room');
});

test('Start game', async t => {
    await t
        .typeText('#screen-name', screen_name)
        .typeText('#room-id', room_id)
        .click('#submit-button')
        .wait(3000)
        .click('#start-game');
});

test('Load game board', async t => {
    await t
        .typeText('#screen-name', screen_name)
        .typeText('#room-id', room_id)
        .click('#submit-button')
        .click('#start-game');

    const btnReveal = Selector('.reveal');
    const reveal = await btnReveal.with({ visibilityCheck: true })();
});

// Having some trouble with this one.
test('Roll dice', async t => {
    await t
        .typeText('#screen-name', screen_name)
        .typeText('#room-id', room_id)
        .click('#submit-button')
        .click('#start-game')

    const diceSelector = Selector('#confirm')
    const rollDice = await diceSelector.with({ visibilityCheck: true})();

    await t
        .click(diceSelector);
});

/*test('Reveal & use special', async t => {
    await t
        .typeText('#screen-name', screen_name)
        .typeText('#room-id', room_id)
        .click('#submit-button')
        .click('#start-game')
        .wait(5000)
        .click('#reveal')
        .wait(1000)
        .click('#special');
});*/
