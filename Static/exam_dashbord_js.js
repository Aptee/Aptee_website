//time function call
var display = document.querySelector('#time');
 //time function
 function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    openFullscreen()
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
            //next_q('1')
            document.getElementById("submit_btn").click();  

        }
    }, 1000);
}

var elem = document.getElementById("main_bd");
function openFullscreen() {
    console.log('yo')
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.webkitRequestFullscreen) { /* Safari */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) { /* IE11 */
    elem.msRequestFullscreen();
  }
}