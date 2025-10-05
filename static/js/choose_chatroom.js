let choose_new = document.getElementById("add");
let password = document.getElementById("room_password")
choose_new.addEventListener("keypress", function (event) {
    if (event.key == "Enter") {

        window.location.href = "/chatroom/choose_chatroom/" + choose_new.value;
    }
})

function chose(element) {
    window.location.href = "/chatroom/choose_chatroom/" + element.value;

}

window.chose = chose;