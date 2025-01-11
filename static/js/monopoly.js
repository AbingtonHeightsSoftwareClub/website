import * as mono from "./monopoly_functions.js";
const socket = io({autoConnect: false});
document.getElementById("join").addEventListener("click", function () {
    socket.connect();
    socket.on("join", (message) => {
    console.log(message.message);
});
    document.getElementById("join").remove();
})

socket.on("test_complete") => {
console.log("good");
}
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

let speed = 10;
var tile = 0;
let overLay = 1;
let overLayElements = document.querySelectorAll(".corner, .tile, .rtile, .ltile");

mono.moveTo(monopoly_1, 0);
mono.input(document, monopoly_1, speed, overLayElements, tile, overLay);
