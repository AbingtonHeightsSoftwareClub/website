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
    span.classList.add("span");
    item.classList.add("item");


    // for the rightmost elements
    if (i >= 9 && i <= 26) {
        if (i % 2 === 0) {
            // Rotates tiles on the right side, so the text faces the correct way
            span.classList.add("right")
            item.id = String(32 + (i - 10) / 2);
        } else {
            // Rotates tiles on the left  side, so the text faces the correct way
            span.classList.add("left");
            item.id = String(24 - (i - 1) / 2);

        }
    }
    // Sets the id, so javascript can reference it easily
    if (i <= 8) {
        item.id = String(22 + i);
    } else if (i > 26) {
        item.id = String(10 - (i - 27));
    }

    // Adds the text to the span
    span.textContent = item.id;
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
    console.log(data.properties);
    // loop through all bottom tiles and append tooltip to them
    for (let i = 1; i < 41; i++) {
        let tile = document.getElementById(String(i));
        console.log(tile);
        let tooltipText = document.createElement("div")
        tooltipText.classList.add("tooltip-text")
        tooltipText.textContent = "Property Name"; // REPLACE ASAP!!!!!!!!!!!!!
        tile.append(tooltipText);
    }
});


// When the server responds to the user rolling, the user what it rolls and moves the player accordingly
socket.on("rolled", (data) => {
    display.innerHTML = JSON.stringify(data);

    let current_position = data["current_position"];
    // Player rolled and should be put on this tile
    let tile_to_go_to = document.getElementById(data["current_position"]);
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




