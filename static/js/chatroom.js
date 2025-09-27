const socket = io({autoConnect: true});

// grab all of the required elements from chatroom.html
const chatForm = document.getElementById("chat-form");
const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message-input");
const userCount = document.getElementById("user-count");
const typingBar = document.getElementById("typing-bar");

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

socket.on('chatroom-join', (data) => {
    sendChatMessage(data.message);

    // data.user is the string of the username, NOT the object
    let currentUser = data.user;
    // if the user isn't already in the list of connected users
    if(!document.getElementById(currentUser)) {
        // make a new div for the user's name in the user-count tab
        const userIndicator = document.createElement('div');
        userIndicator.id = currentUser;
        userIndicator.textContent = currentUser;
        userCount.appendChild(userIndicator)
    }
});

socket.on('disconnect', (reason) => {
    console.log('Socket disconnected:', reason);
});

socket.on('leave', (data) => {
    sendChatMessage(data.message);

    // data.user is the string of the username, NOT the object
    let currentUser = data.user;
    // if the user is already in the list of connected users
    if(document.getElementById(currentUser)) {
        // remove the current user
        let userIndicator = document.getElementById(currentUser);
        userIndicator.remove();
    }
});

// Server emits broadcast-message in chatroom_sockets.py
socket.on('broadcast-message', (data) => {
    // Remove the typing notification when they send a message
    if(document.getElementById((data.user + "-typing"))) {
        document.getElementById((data.user + "-typing")).remove();
    }
    sendChatMessage(data.user + ": " + data.message);
});

// Server emits broadcast-message in chatroom_sockets.py
socket.on('load-messages', (data) => {
    chatBox.replaceChildren();

    data["messages"].forEach(message => {
        sendChatMessage(message.user + ": " + message.message);

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
})