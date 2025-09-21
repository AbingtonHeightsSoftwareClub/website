const socket = io({autoConnect: true});

const display = document.getElementById("console");
const grid = document.getElementsByClassName("board")[0];
for (let i = 0; i < 36; i++) {
    let item = document.createElement("div")
    let span = document.createElement("span");
    span.textContent = String(i)
    item.classList.add("item");

    if (i >= 9 && i <= 26) {
        if (i % 2 === 0) {
            span.classList.add("right")
        } else {
            span.classList.add("left");

        }
    }

    item.id = String(i);
    item.append(span);
    grid.append(item);
}


socket.on("join", (data) => {
    console.log(data.message);
    display.innerHTML = data.message + " Press R to roll.";

});

socket.on("rolled", (data) => {


    display.innerHTML = JSON.stringify(data);

    document.getElementById(data["current_position"]).children[0].append(player);


});


const player = document.createElement('img');
player.src = "/static/img/monopoly_piece_1.svg";
player.id = "monopoly-1";
player.className = "piece";

document.getElementById("2").appendChild(player);


document.addEventListener("keydown", function (event) {
    // Check the key code of the pressed key
    switch (event.code) {
        case "KeyR":
            socket.emit("roll");

            break;
    }


});




