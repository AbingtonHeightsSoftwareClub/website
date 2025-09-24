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

// debugging stuff to prevent more future headaches
socket.on('connect', () => {
    console.log('Socket connected:', socket.id);
});

socket.on('disconnect', (reason) => {
    console.log('Socket disconnected:', reason);
});

// Server emits broadcast-message in chatroom_sockets.py
socket.on('broadcast-message', (data) => {
    console.log('Received broadcast-message:', data);
    // create the div for the message on all clients
    const messageElement = document.createElement('div');
    messageElement.className = 'chat-message';

    // create the text of the message on all clients
    const body = document.createElement('div');
    body.className = 'chat-message-body';
    body.textContent = data.user + ": " + data.message;

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
});