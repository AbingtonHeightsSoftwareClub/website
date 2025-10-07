const socket = io({autoConnect: true});

let choose_new = document.getElementById("add");
let password = document.getElementById("new-room-password")

choose_new.addEventListener("keypress", function (event) {
    if (event.key == "Enter") {

        window.location.href = "/chatroom/choose_chatroom/" + choose_new.value;
    }
})

password.addEventListener("keypress", function (event) {
    if (event.key == "Enter") {
        console.log(password.value)
        socket.emit('private-room-creation', password.value, choose_new.value);
        window.location.href = "/chatroom/choose_chatroom/" + choose_new.value;
    }
})

// chose now has 2nd bool parameter password
function chose(element, password) {
    // if it's not a private room, send them to the room
    if (!password)
        window.location.href = "/chatroom/choose_chatroom/" + element.value;
    // if it is a private room, check with the server to see if they know the password
    else {
        let roomID = element.value
        let passwordToCheck = document.getElementById("room-password-" + roomID).value
        console.log(passwordToCheck, roomID)
        socket.emit("room-password-check", roomID, passwordToCheck);
    }
}

// once the server responds with the password result
socket.on('room-password-result', (data) => {
    // send them in if they get it right
    if (data.password_matches) {
        window.location.href = "/chatroom/choose_chatroom/" + data.room_id;
    }
    // tell them to try again if they don't
    else {
        alert("Incorrect password.");
        window.location.href = "/chatroom/choose_chatroom/choose";
    }
});

window.chose = chose;