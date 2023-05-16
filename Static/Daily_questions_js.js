const start_btn = document.querySelector(".start_btn button");
const info_box = document.querySelector(".info_box");
var startTime;
start_btn.onclick = ()=>{
    info_box.classList.add("activeInfo"); //show info box
    startTime = Date.now();
    console.log(Date.now);
}

function stopButton() {
    if (startTime) {
        var endTime = Date.now();
        var difference = endTime - startTime - 200;
        document.getElementById("feild_txt").value = difference;
        console.log(difference);
        startTime = null;
    } else {
        alert('Click the Start button first');
    }
}

function startButton(){
    alert("Hello");
}