const gameBoard = document.querySelector("#gameboard");
const playerDisplay = document.querySelector("#player");
const infoDiplay = document.querySelector("#info-display");

const pieces = [
    "c", "t", "t", "t", "t", "t", "t", "t", "t", "t", "c",
    "lt", "center", "rt",
    "lt", "center", "rt",
    "lt", "center", "rt",
    "lt", "center", "rt",
    "lt", "center", "rt",
    "lt", "center", "rt",
    "lt", "center", "rt",
    "lt", "center", "rt",
    "lt", "center", "rt",
    "c", "t", "t", "t", "t", "t", "t", "t", "t", "t", "c",

]

const ids = [
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
    20,                                     32,
    19,                                     33,
    18,                                     34,
    17,                                     35,
    16,                                     36,
    15,                                     37,
    14,                                     38,
    13,                                     39,
    12,                                     40,
    11, 10,  9,  8,  7,  6,  5,  4,  3,  2,  1
]


function createBoard() {
  let j=0;
  for (let i=0; i<pieces.length; i++){
    const tile = document.createElement("div");

    switch(pieces[i]){
        case "c":
            tile.classList.add("corner");
           
            tile.id=ids[j]-1;
            j+=1;
            break;
        case "t":
            tile.classList.add("tile");
            tile.id=ids[j]-1;
            j+=1;

            break;
        case "lt":
            tile.classList.add("ltile");
            tile.id=ids[j]-1;
            j+=1;

            break;
        case "center":
            tile.classList.add("center");
            break;
        case "rt":
            tile.classList.add("rtile");
            tile.id=ids[j]-1;
            j+=1;

            break;
        default:
            console.error("Error");
            break;
        
    }
    
    gameBoard.append(tile);
  }
}

createBoard();
