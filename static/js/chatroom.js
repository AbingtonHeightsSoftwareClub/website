const socket = io({autoConnect: true});

// grab all of the required elements from chatroom.html
const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message-input");
const userCount = document.getElementById("user-count");
const typingBar = document.getElementById("typing-bar");

chatForm.addEventListener("submit", function (event) {
    // stops the form from refreshing the page on submit
    event.preventDefault();
    // declare text without unnessecary whitespace
    const text = messageInput.value.trim();
    // don't add empty messages
    if (!text) return;
    let time = new Date().toLocaleTimeString()
    // for debugging
    console.log('Emitting message-sent:', text);
    // send the server the message
    socket.emit("message-sent", text, time)
    // clear input and focus after sending so that they can send more messages quickly
    messageInput.value = '';
    messageInput.focus();
});

chatForm.addEventListener("input", function(event){
    // stops the form from refreshing the page on input
    event.preventDefault();
    socket.emit("typing-event");
});

chatForm.addEventListener("focusout", function(event) {
    // stops the form from refreshing the page when the input loses blur
    event.preventDefault();
    socket.emit("typing-stopped");
});

function sendChatMessage(message, time) {
    // create the div for the join message on all clients
    const messageElement = document.createElement('div');
    messageElement.className = 'chatroom-message';

    // time SHOULD always exist
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

socket.on('chatroom-join', (data) => {
    sendChatMessage(data.message);

    // Iterates through every active user and appends to list of current users
    data["users"].forEach(user => {
        // If the user is not already in the active user table, put them in.
        if (document.getElementById(user.id) == null) {
            let userIndicator = document.createElement('div');
            userIndicator.id = user.id;
            userIndicator.textContent = user.title;
            userCount.appendChild(userIndicator);
        }

    })


});

socket.on('disconnect', (reason) => {
    console.log('Socket disconnected:', reason);
});

socket.on('leave', (data) => {
    sendChatMessage(data.message);

    // If the user is on the list of those connect, remove that user that left.
    if (document.getElementById(data.id) != null) {
        // If the user that left is in the connected section, that user will be removed.
        let userIndicator = document.getElementById(data.id);
        userIndicator.remove();
    }

});

// Server emits broadcast-message in chatroom_sockets.py
socket.on('broadcast-message', (data) => {
    // Remove the typing notification when they send a message
    if(document.getElementById((data.user + "-typing"))) {
        document.getElementById((data.user + "-typing")).remove();
    }
    sendChatMessage(data.user + ": " + data.message, data.time);
});

// Server emits broadcast-message in chatroom_sockets.py
socket.on('load-messages', (data) => {
    chatBox.replaceChildren();

    data["messages"].forEach(message => {
        sendChatMessage(message.user + ": " + message.message, message.time);

    })
});

socket.on('typing-event', (data) => {
    const currentUser = data.user;
    const message = currentUser + " is typing...";
    // If there is not already a notification that the user is typing
    if(!document.getElementById((currentUser + "-typing"))) {
        // Create a notification that the user is typing
        const typingMessage = document.createElement("div");
        typingMessage.id = currentUser + "-typing";
        typingMessage.className = "typing-bar";
        typingMessage.textContent = message;
        typingBar.appendChild(typingMessage);
    }
});

socket.on('typing-stopped', (data) => {
    // Remove the typing notification when they unfocus the chatbar
    if(document.getElementById((data.user + "-typing"))) {
        document.getElementById((data.user + "-typing")).remove();
    }
});