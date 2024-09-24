'use strict';



const diceEl = document.querySelector(".dice");
const rollDiceBtn = document.querySelector(".btn--roll");
const holdBtn = document.querySelector(".btn--hold");
const newBtn = document.querySelector(".btn--new");
const player0El = document.querySelector('.player--0');
const player1El = document.querySelector('.player--1');

let currentScore = 0;
let activePlayer = 0;

const scores = [0,0];

diceEl.classList.add('hidden');

const rollDice = function () {

    if(scores[0]<100 && scores[1]<100){
    
    diceEl.classList.remove('hidden');

    const dice = Math.trunc(Math.random()*6) + 1;

    diceEl.src = `dice-${dice}.png`;

    if(dice == 1)
    {
        currentScore = 0;
        document.getElementById(`current--${activePlayer}`).textContent = currentScore;
        activePlayer = activePlayer == 0?1:0;
        player0El.classList.toggle('player--active');
        player1El.classList.toggle('player--active');
    }
    else{
        currentScore+= dice;
        document.getElementById(`current--${activePlayer}`).textContent = currentScore;
    }
}
    
}

const holdScores = function () {
    if(scores[0]<100 && scores[1]<100){

    scores[activePlayer] += currentScore;
    currentScore = 0;
    document.getElementById(`current--${activePlayer}`).textContent = currentScore;
    document.getElementById(`score--${activePlayer}`).textContent = scores[activePlayer];
    if(scores[activePlayer]<100){
    activePlayer = activePlayer == 0?1:0;
    player0El.classList.toggle('player--active');
    player1El.classList.toggle('player--active');
    }
    else{

        const activeP = document.querySelector('.player--active')
        activeP.classList.add('player--winner');
    }
    
    }
}

const reset = function () {
    
    currentScore = 0;
    scores[0] = 0;
    scores[1] = 0;
    activePlayer = 0;
    document.getElementById('score--0').textContent = 0;
    document.getElementById('score--1').textContent = 0;
    document.getElementById('current--0').textContent = 0;
    document.getElementById('current--1').textContent = 0;
    player1El.classList.remove('player--active');
    player1El.classList.remove('player--winner');
    player0El.classList.add('player--active');
    diceEl.classList.add('hidden');

}

rollDiceBtn.addEventListener('click', rollDice);

holdBtn.addEventListener('click', holdScores);

newBtn.addEventListener('click', reset);