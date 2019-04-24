import { Selector } from 'testcafe';

fixture `Concurrency`
    .page `localhost:5000`;

const screen_name = 'amritrau'
const room_id = 'akw200'

function randomId() {
  return Math.random().toString(36).substr(2, 5);
}


test('Start game simultaneously', async t => {
    await t
        .typeText('#screen-name', randomId())
        .typeText('#room-id', room_id)
        .click('#submit-button')
        .wait(1000)
        .click('#start-game')
        .wait(2500);
});
