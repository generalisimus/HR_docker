
document.addEventListener('DOMContentLoaded', () => {

	const answerList = document.querySelector('.answer'),
		  answerError = document.querySelector('.answer_error')
		  pollList = document.querySelector('#answer_polling'),
		  startTimerPollSecond = document.querySelector('#seconds'),
		  startTimerPollMinutes = document.querySelector('#minutes'),
		  startTimerQuestion = document.querySelector('#timer_question'),
		  answerClick = document.querySelector('#answer_question'),
		  inputTime = document.querySelector('.input_time'),
		  timerPoll = document.querySelector('#timer_poll'),
		  createList = document.querySelector('.form-check');

	  
	if(timerPoll) {

		let countdownsecond = localStorage["currentTimeSecond"] || startTimerPollSecond.innerHTML;
			countdownminutes = localStorage["currentTimeMinutes"] || startTimerPollMinutes.innerHTML;

		if (answerList) {
			getTimer();
			timer = setInterval(getTimer, 1000);
		} 
		function getTimer() {
			startTimerQuestion.innerHTML--;
			localStorage['currentTimeSecond'] = countdownsecond;
			startTimerPollSecond.innerHTML = countdownsecond;
			countdownsecond--;
			localStorage["currentTimeMinutes"] = countdownminutes;
			startTimerPollMinutes.innerHTML = countdownminutes;
			if (startTimerPollSecond.innerHTML.length < 2) {
				startTimerPollSecond.innerHTML = '0' + startTimerPollSecond.innerHTML;
			}


			if (countdownsecond == 0 && countdownminutes == 0) {
				countdownsecond = 0;
				countdownminutes = 0;
				localStorage.removeItem("currentTimeMinutes");
				localStorage.removeItem("currentTimeSecond");
				answerList.style.display = 'none';
				answerError.style.display = 'flex';			
			}
			if (countdownsecond <= 0) {
				countdownminutes--;
				countdownsecond = 60;
			}
			if (countdownminutes < 0 || startTimerQuestion.innerHTML == 0) {
					countdownsecond = 0;
					countdownminutes = 0;
					answerList.style.display = 'none';
					answerError.style.display = 'flex';		
					clearInterval(timer);
				//	localStorage.clear();
			}

				//localStorage.removeItem("currentTimeSecond");



		}

	}
	if (!answerList) {
		localStorage.removeItem("currentTimeMinutes");
		localStorage.removeItem("currentTimeSecond");
	}

});


