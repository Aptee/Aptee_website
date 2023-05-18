//time function call
var fiveMinutes = 60 * 30,
        display = document.querySelector('#time');
function fun(){
    show_q();
    startButton();
    startTimer(fiveMinutes, display);
}

// first question upload
function show_q(){
    const start_btn = document.querySelector(".start_btn button");
    const info_box = document.querySelector(".info_box");
    start_btn.onclick = ()=>{
    info_box.classList.add("activeInfo"); //show info box
    }
}

// first question status
function startButton() {
    var element = document.getElementById("one");
    element.classList.add("q_status");
 }

 //time function
 function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            timer = duration;
            next_q();
            document.getElementById("submit_btn").click();
        }
    }, 1000);
}
