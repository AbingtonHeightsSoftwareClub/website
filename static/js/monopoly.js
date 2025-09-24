// Connects client to server for communication 
const socket = io({autoConnect: true});

// Since chromebooks disable inspection, since is a fake console. display references that text.
const display = document.getElementById("console");

// grid references the monopoly board
const grid = document.getElementsByClassName("board")[0];
for (let i = 0; i < 36; i++) {
    // Adds tiles to monopoly, except for the already defined corners.

    // Item is the tile
    let item = document.createElement("div");
    // Span is the text that has the id
    let span = document.createElement("span");

    // Sets the text in the tile to its id, but since corners are not accounted for, its not completely accurate.
    span.textContent = String(i)
    item.classList.add("item");

    if (i >= 9 && i <= 26) {
        if (i % 2 === 0) {
            // Rotates tiles on the right side, so the text faces the correct way
            span.classList.add("right")
        } else {
            // Rotates tiles on the left  side, so the text faces the correct way
            span.classList.add("left");

        }
    }
    // Sets the id, so javascript can reference it easily
    item.id = String(i);

    // Adds the text to the tiles
    item.append(span);
    // Adds the tile to the grid
    grid.append(item);
}

// Creates an image that is the player
const player = document.createElement('img');
// Makes the image a hat
player.src = "/static/img/monopoly_piece_1.svg";
// Lets javascript know what the player is referenced as
player.id = "monopoly-1";
// Gives the player a class, so the CSS makes it pretty
player.className = "piece";

// Starts by putting the player in tile 2
document.getElementById("2").appendChild(player);


// When the server responds to the user happening, this code is ran.
socket.on("join", (data) => {
    console.log(data.message);
    display.innerHTML = data.message + " Press R to roll.";

});


// When the server responds to the user rolling, the user what it rolls and moves the player accordingly
socket.on("rolled", (data) => {
    display.innerHTML = JSON.stringify(data);

    let current_position = data["current_position"]);
    // Player rolled and should be put on this tile
    let tile_to_go_to =  document.getElementById(data["current_position"]);
    // Player should be oriented the same as the text, so we put it in the span, with is called the child of the tile
    let span = document.getElementById(data["current_position"]).children[0];

    // Puts player into the span
    span.append(player);
});




// When the user presses r, the user tells the server to roll its player
document.addEventListener("keydown", function (event) {
    // Check the key code of the pressed key
    switch (event.code) {
        case "KeyR":
            socket.emit("roll");

            break;
    }


});




