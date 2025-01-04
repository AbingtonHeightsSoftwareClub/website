
const socket = io({autoConnect: true});
let username = "Seamus";
socket.on("connect", function () {
    socket.emit("user_join", username)
})

document.getElementById("join").addEventListener("click", function () {
    


})