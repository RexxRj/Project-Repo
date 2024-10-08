'use strict';

let secretNumber = Math.trunc(Math.random()*20) + 1;

let score = Number(document.querySelector('.score').textContent);
let highscore = Number(document.querySelector('.Highscore').textContent);

const initialScore = score;
const initialMessage = document.querySelector('.message').textContent;
const initialBackground = document.querySelector('body').style.backgroundColor;
const initalWidth = document.querySelector('.number').style.width;

const modal = document.querySelector('.modal');
const closeModal = document.querySelector('.close-modal');

const gameLogic = function () {

    const guess = Number(document.querySelector('.guess').value);

    if (score==1)
        {
            document.querySelector('.message').textContent = "🎮 Game Over!"
            score--;
            document.querySelector('.score').textContent = score;
        }
    else if(document.querySelector('.number').textContent == '?' && score>0)
    {
        if(!guess){
            document.querySelector('.message').textContent = "⛔ Not a number!"
            score--;
            document.querySelector('.score').textContent = score;     
        }       
        else if (guess>secretNumber){
            document.querySelector('.message').textContent = "📈 Too High!"
            score--;
            document.querySelector('.score').textContent = score;
        }
        else if (guess<secretNumber){
            document.querySelector('.message').textContent = "📉 Too Low!"
            score--;
            document.querySelector('.score').textContent = score;
        }
        else
        {
            document.querySelector('.message').textContent = "🎉 Correct Guess!";
            document.querySelector('body').style.backgroundColor = '#6fe873';
            document.querySelector('.number').style.width = '30rem';
            document.querySelector('.score').textContent = score;
            document.querySelector('.number').textContent = secretNumber;
            highscore = score>highscore?score:highscore;
            document.querySelector('.Highscore').textContent = highscore;
        }
    }

}

document.querySelector('.check').addEventListener('click', gameLogic)
document.querySelector('.guess').addEventListener('keydown', 
    function(e) {
        if(e.key === 'Enter') gameLogic();
    }
)

document.querySelector('.again').addEventListener(

    'click', function() {

        document.querySelector('.message').textContent = initialMessage;
        document.querySelector('.number').style.width = initalWidth;
        document.querySelector('body').style.backgroundColor = initialBackground;
        document.querySelector('.score').textContent = initialScore;
        score = initialScore;
        document.querySelector('.number').textContent = '?';
        document.querySelector('.guess').value = '';
        secretNumber = Math.trunc(Math.random()*20) + 1;
    }
)

document.querySelector('.info').addEventListener('click',
    function(){
        modal.classList.remove('hidden');
    }
)

closeModal.addEventListener('click',
    function() {
        if(!modal.classList.contains('hidden')) modal.classList.add('hidden')
    }
)