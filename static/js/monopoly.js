import * as mono from "./monopoly_functions.js";

const gameBoard = document.querySelector("#gameboard");
const playerDisplay = document.querySelector("#player");
const infoDiplay = document.querySelector("#info-display");

const pieces = [
    "c",
    "t",
    "t",
    "t",
    "t",
    "t",
    "t",
    "t",
    "t",
    "t",
    "c",
    "lt",
    "center",
    "rt",
    "lt",
    "center",
    "rt",
    "lt",
    "center",
    "rt",
    "lt",
    "center",
    "rt",
    "lt",
    "center",
    "rt",
    "lt",
    "center",
    "rt",
    "lt",
    "center",
    "rt",
    "lt",
    "center",
    "rt",
    "lt",
    "center",
    "rt",
    "c",
    "t",
    "t",
    "t",
    "t",
    "t",
    "t",
    "t",
    "t",
    "t",
    "c",
];

const ids = [
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 20, 32, 19, 33, 18, 34, 17, 35,
    16, 36, 15, 37, 14, 38, 13, 39, 12, 40, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1,
];

mono.createBoard(pieces, gameBoard, ids);

let monopoly_1 = document.getElementById("monopoly-1");
monopoly_1.style.position = "absolute"; // Ensure it's absolutely positioned
monopoly_1.style.left = "0px"; // Initialize left position
monopoly_1.style.top = "0px"; // Initialize top position

let speed = 10;
let tile = -1;
let overLay = 1;
let overLayElements = document.querySelectorAll(".corner, .tile, .rtile, .ltile");


mono.input(document, monopoly_1, speed, overLayElements, tile, overLay);

// document.addEventListener("keydown", function (event) {
//     // Check the key code of the pressed key
//     switch (event.key) {
//         case "ArrowUp":
//             mono.upHandler(monopoly_1, speed);
//             break;
//         case "ArrowDown":
//             mono.downHandler(monopoly_1, speed);
//             break;
//         case "ArrowLeft":
//             mono.leftHandler(monopoly_1, speed);
//             break;
//         case "ArrowRight":
//             mono.rightHandler(monopoly_1, speed);
//             break;
//         default:
//             break;
//     }
//     switch (event.code) {
//         case "KeyA":
//             tile += 1;
//             tile %= 40;
//             mono.moveTo(monopoly_1, tile);

//             break;
//         case "KeyD":
//             tile -= 1;
//             if (tile < 0) {
//                 tile = 40 + tile;
//             }
//             tile % 40;
//             mono.moveTo(monopoly_1, tile);
//             break;
//         case "KeyL":
//             overLay *= -1;
//             for (let i = 0; i < overLayElements.length; i++) {
//                 if (overLay==1){
//                 overLayElements[i].style.visibility = "visible";

//                 }else{
//                     overLayElements[i].style.visibility = "hidden";
//                 }
//             }
//             break;
//     }
// });
