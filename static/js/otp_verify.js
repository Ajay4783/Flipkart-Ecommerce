let timeLeft = 30;
const timerDisplay = document.getElementById('countdown-timer');
const resendLink = document.getElementById('resend-link');

const countdown = setInterval(() => {
    if (timeLeft <= 0) {
        clearInterval(countdown);

        timerDisplay.style.display = 'none';
        resendLink.style.display = 'inline';
    } else {

        let seconds = timeLeft < 10 ? '0' + timeLeft : timeLeft;
        timerDisplay.innerText = "00:" + seconds;
        timeLeft -= 1;
    }
}, 1000); 
