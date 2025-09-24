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

    // create a new element to display the requested message
    const messageElement = document.createElement('div'); 
    // assign its class 
    messageElement.className = 'chat-message'; 
    // give it the text 
    messageElement.textContent = text; 
    // append it instead of assigning it so that it doesn't replace it or anything 
    chatBox.appendChild(messageElement); 

    // scroll to bottom 
    chatBox.scrollTop = chatBox.scrollHeight; 

    // clear input and focus so if they wanna send more they can do so quickly 
    messageInput.value = ''; 
    messageInput.focus(); 
});