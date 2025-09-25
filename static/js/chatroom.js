const socket = io({autoConnect: true});

// grab all of the required elements from chatroom.html
const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message-input");

chatForm.addEventListener("submit", function(event) {
    // stops the form from refreshing the page on submit
    event.preventDefault();
    // declare text without unnessecary whitespace
    const text = messageInput.value.trim(); 
    // don't add empty messages
    if (!text) return; 

    // for debugging
    console.log('Emitting message-sent:', text);
    // send the server the message
    socket.emit("message-sent", text)
    // clear input and focus after sending so that they can send more messages quickly
    messageInput.value = '';
    messageInput.focus();
});

function sendChatMessage(message) {
    // create the div for the join message on all clients
    const messageElement = document.createElement('div');
    messageElement.className = 'join-message';
    
    let time = new Date().toLocaleTimeString(); // Ex. 11:18:48 AM
    const timestamp = document.createElement('span');
    timestamp.className = 'timestamp';
    timestamp.textContent = time;
    messageElement.appendChild(timestamp);

    // create the text of the message on all clients
    const body = document.createElement('div');
    body.className = 'message-body';
    body.textContent = message;
    messageElement.appendChild(body);
    // make sure the chatbox is there before appending 
    if (chatBox) {
        chatBox.appendChild(messageElement);
    // if it ain't there then don't try to append nothin
    } else {
        console.warn('chatBox not available; dropping message', data);
    }
    // in case too many messages to fit the box
    chatBox.scrollTop = chatBox.scrollHeight;
}
// debugging stuff to prevent more future headaches
socket.on('connect', () => {
    socket.emit("load-messages", socket.id)  
    console.log('Socket connected:', socket.id);
});

socket.on('join', (data) => {
    sendChatMessage(data.message);
});

socket.on('disconnect', (reason) => {
    console.log('Socket disconnected:', reason);
});

socket.on('leave', (data) => {
    sendChatMessage(data.message);
});

// Server emits broadcast-message in chatroom_sockets.py
socket.on('broadcast-message', (data) => {
    sendChatMessage(data.user + ": " + data.message);
});