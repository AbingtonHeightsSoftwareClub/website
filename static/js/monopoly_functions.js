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

export function leftHandler(monopoly_1, speed) {
    let currentLeft = parseInt(monopoly_1.style.left, 10); // Get current left position
    monopoly_1.style.left = currentLeft - speed + "px"; // Move left by speed (negative direction)
    console.log(monopoly_1.style.left);
}

export function rightHandler(monopoly_1, speed) {
    let currentLeft = parseInt(monopoly_1.style.left, 10); // Get current left position
    monopoly_1.style.left = currentLeft + speed + "px"; // Move right by speed (positive direction)
    console.log(monopoly_1.style.left);
}

export function upHandler(monopoly_1, speed) {
    let currentTop = parseInt(monopoly_1.style.top, 10); // Get current top position
    monopoly_1.style.top = currentTop - speed + "px"; // Move up by speed (negative direction)
    console.log(monopoly_1.style.top);
}

export function downHandler(monopoly_1, speed) {
    let currentTop = parseInt(monopoly_1.style.top, 10); // Get current top position
    monopoly_1.style.top = currentTop + speed + "px"; // Move down by speed (positive direction)
    console.log(monopoly_1.style.top);
}

export function moveTo(monopoly_1, tile) {
    let pos = getElementCenter(document.getElementById(tile));
    console.log(pos);
    monopoly_1.style.left = pos.x + "px";
    monopoly_1.style.top = pos.y + "px";
}



export function getElementCenter(element) {
    const rect = element.getBoundingClientRect();

    return { x:rect.left + rect.width/2-50/2, y:rect.top + rect.height/2-50/2};
}

export function input(document, monopoly_1, speed, overLayElements, tile, overLay){
    document.addEventListener("keydown", function (event) {
        // Check the key code of the pressed key
        switch (event.key) {
            case "ArrowUp":
                upHandler(monopoly_1, speed);
                break;
            case "ArrowDown":
                downHandler(monopoly_1, speed);
                break;
            case "ArrowLeft":
                leftHandler(monopoly_1, speed);
                break;
            case "ArrowRight":
                rightHandler(monopoly_1, speed);
                break;
            default:
                break;
        }
        switch (event.code) {
            case "KeyA":
                tile += 1;
                tile %= 40;
                moveTo(monopoly_1, tile);
    
                break;
            case "KeyD":
                tile -= 1;
                if (tile < 0) {
                    tile = 40 + tile;
                }
                tile % 40;
                moveTo(monopoly_1, tile);
                break;
            case "KeyL":
                overLay *= -1;
                for (let i = 0; i < overLayElements.length; i++) {
                    if (overLay==1){
                    overLayElements[i].style.visibility = "visible";
    
                    }else{
                        overLayElements[i].style.visibility = "hidden";
                    }
                }
                break;
        }
    });
}