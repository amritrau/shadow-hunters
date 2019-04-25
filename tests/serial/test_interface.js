import { Selector } from 'testcafe';

fixture `Interface`
    .page `localhost:5000`;

const screen_name = 'amritrau'
const room_id = 'akw200'


test('Send message', async t => {
    await t
        .typeText('#screen-name', screen_name)
        .typeText('#room-id', room_id)
        .click('#submit-button');

    const location = await t.eval(() => window.location);
    await t
        .expect(location.pathname).eql('/room')
        .click('#start-game');
        .wait(5000)
        .typeText('#message', "Hello, world!")
        .click('.send')
        .wait(2500);
});
