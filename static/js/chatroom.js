const socket = io({autoConnect: true});
const display = document.getElementById("message-board");
const chatForm = document.getElementById("chat-form");
const messageField = document.getElementById("message-field");

socket.on("message", (data) => {
    display.innerText = data.message;
});

chatForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const message = messageField.value.trim();
    if (message.length > 0) {
        socket.emit("message", message);
        messageField.value = "";
    }
});