export function createBoard(pieces, gameBoard, ids) {
    let j = 0;
    for (let i = 0; i < pieces.length; i++) {
        const tile = document.createElement("div");

        switch (pieces[i]) {
            case "c":
                tile.classList.add("corner");

                tile.id = ids[j] - 1;
                j += 1;
                break;
            case "t":
                tile.classList.add("tile");
                tile.id = ids[j] - 1;
                j += 1;

                break;
            case "lt":
                tile.classList.add("ltile");
                tile.id = ids[j] - 1;
                j += 1;

                break;
            case "center":
                tile.classList.add("center");
                break;
            case "rt":
                tile.classList.add("rtile");
                tile.id = ids[j] - 1;
                j += 1;

                break;

            default:
                console.error("Error");
                break;
        }

        gameBoard.append(tile);
    }
}


export function moveTo(monopoly_1, tile) {
    let pos = document.getElementById(tile);
    pos.appendChild(monopoly_1);
    let size = "1rem";
    monopoly_1.style.top = "0rem";
    monopoly_1.style.bottom = "0rem";
    monopoly_1.style.left = "0rem";
    monopoly_1.style.right = "0rem";
    if (0 <= tile && tile <= 10) {
        monopoly_1.style.top=size;


    } else if (11 <= tile && tile <= 20) {
        monopoly_1.style.left="-1rem";

    } else if (21 <= tile && tile <= 30) {
        monopoly_1.style.top="-1.5rem";
    } else {
        monopoly_1.style.left=size;
    }

}



export function input(document, monopoly_1, overLayElements, tile, overLay, socket) {
    document.addEventListener("keydown", function (event) {
        // Check the key code of the pressed key
        switch (event.code) {
            case "KeyA":
                tile += 1;
                tile %= 40;
                moveTo(monopoly_1, tile);
                socket.emit("roll", {"position": tile})

                break;
            case "KeyD":
                tile -= 1;
                if (tile < 0) {
                    tile = 40 + tile;
                }
                tile % 40;
                moveTo(monopoly_1, tile);
                socket.emit("roll", {"position": tile})
                break;
            case "KeyL":
                overLay *= -1;
                for (let i = 0; i < overLayElements.length; i++) {
                    if (overLay == 1) {
                        overLayElements[i].style.visibility = "visible";

                    } else {
                        overLayElements[i].style.visibility = "hidden";
                    }
                }
                break;
        }

        
    });
}

