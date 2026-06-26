let attempts = 9;
let number = [];

window.onload = function () {
    init();
}

function init() {
    attempts = 9;
    number = [];

    while (number.length < 3) {
        let num = Math.floor(Math.random() * 10);

        if (!number.includes(num)) {
            number.push(num)
        }
    }

    document.getElementById('number1').value = '';
    document.getElementById('number2').value = '';
    document.getElementById('number3').value = '';
    document.getElementById('attempts').textContent = attempts;
    document.getElementById('results').innerHTML = '';

    const Btn = document.querySelector('.submit-button');
    if (Btn) {
        Btn.disabled = false;
    }

    document.getElementById('number1').disabled = false;
    document.getElementById('number2').disabled = false;
    document.getElementById('number3').disabled = false;
}

function check_numbers() {
    let number1 = document.getElementById('number1').value;
    let number2 = document.getElementById('number2').value;
    let number3 = document.getElementById('number3').value;

    if (number1 == '' || number2 == '' || number3 == '') {
        document.getElementById('number1').value = "";
        document.getElementById('number2').value = "";
        document.getElementById('number3').value = "";
        return;

    }

    const input = [parseInt(number1), parseInt(number2), parseInt(number3)];
    let strike = 0
    let ball = 0;
    let resultHTML;

    for (let i = 0; i < 3; i++) {
        if (input[i] === number[i]) {
            strike++;
        } else if (number.includes(input[i])) {
            ball++;
        }
    }
    attempts--;
    document.getElementById('attempts').textContent = attempts;
    
    if (strike === 0 && ball === 0) {
        resultHTML = `<div class="num-result out">O</div>`;
    }
    else {
        resultHTML = `
        ${strike} <div class="num-result strike">S</div> 
        ${ball} <div class="num-result ball">B</div>
        `;
    }

    document.getElementById('results').innerHTML += `
    <div class='check-result'> 
        <div class='left'>${input.join(" ")}</div>
        <div class='right'>${resultHTML}</div>
    </div>`;

    const Btn = document.querySelector('.submit-button');
    
    let image = document.getElementById('game-result-img');
    
    if (strike === 3) {
        image.src = "success.png";

        if (Btn) {
            Btn.disabled = true;
        }
        document.getElementById('number1').disabled = true;
        document.getElementById('number2').disabled = true;
        document.getElementById('number3').disabled = true;
        return;
    }
    else if (attempts <= 0) {
        image.src = "fail.png";

        if (Btn) {
            Btn.disabled = true;
        }
        document.getElementById('number1').disabled = true;
        document.getElementById('number2').disabled = true;
        document.getElementById('number3').disabled = true;
        return;
    }


    document.getElementById('number1').value = "";
    document.getElementById('number2').value = "";
    document.getElementById('number3').value = "";

}