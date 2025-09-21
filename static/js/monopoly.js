
const display = document.getElementById("console");
const socket = io({ autoConnect: true });


socket.on("join", (data) => {
    console.log(data.message);
    display.innerHTML = data.message + " Press R to roll.";
    const board = document.getElementById("board");
    let nav_height = parseInt(document.defaultView.getComputedStyle(document.getElementsByTagName("nav")[0]).height, 10);
    let console_height = parseInt(document.defaultView.getComputedStyle(document.getElementById("console")).height, 10);
    let window_height = window.screen.height;
    console.log(console_height);
    board.style.scale=String(1-(nav_height+console_height)/window_height);
});

socket.on("rolled", (data) => {


    console.log(data["current_position"]);
    display.innerHTML = JSON.stringify(data);
    document.getElementById(data["current_position"]).appendChild(player);

});



var Tiles = { "List" : [
  {"id":"21" ,"label":"strand", "price":"£220", "icon":"", "color":"red", "order": "2", "pos":"top"},
  {"id":"22" ,"label":"chance", "price":"", "icon":"❓", "color":"none", "order": "3", "pos":"top"},
  {"id":"23" ,"label":"fleet street", "price":"£220", "icon":"", "color":"red", "order": "4", "pos":"top"},
  {"id":"24" ,"label":"trafalgar square", "price":"£240", "icon":"", "color":"none", "order": "5", "pos":"top"},
  {"id":"25" ,"label":"fenchurch st. station", "price":"£200", "icon":"🚂", "color":"none", "order": "6", "pos":"top"},
  {"id":"26" ,"label":"leicester square", "price":"£260", "icon":"", "color":"yellow", "order": "7", "pos":"top"},
  {"id":"27" ,"label":"ceventry street", "price":"£200", "icon":"", "color":"yellow", "order": "8", "pos":"top"},
  {"id":"28" ,"label":"water<br>works", "price":"£150", "icon":"🚰", "color":"none", "order": "9", "pos":"top"},
  {"id":"29" ,"label":"piccadilly", "price":"£280", "icon":"", "color":"yellow", "order": "10", "pos":"top"},
  {"id":"19" ,"label":"vine street", "price":"£200", "icon":"", "color":"orange", "order": "12", "pos":"left"},
  {"id":"18" ,"label":"marlborog'h street", "price":"£200", "icon":"", "color":"orange", "order": "15", "pos":"left"},
  {"id":"17" ,"label":"community chest", "price":"", "icon":"💰", "color":"none", "order": "17", "pos":"left"},
  {"id":"16" ,"label":"bow street", "price":"£180", "icon":"", "color":"orange", "order": "19", "pos":"left"},
  {"id":"15" ,"label":"marylebone station", "price":"£200", "icon":"🚂", "color":"none", "order": "21", "pos":"left"},
  {"id":"14" ,"label":"northumrl'd avenue", "price":"£160", "icon":"", "color":"pink", "order": "23", "pos":"left"},
  {"id":"13" ,"label":"whitehall", "price":"£140", "icon":"", "color":"pink", "order": "25", "pos":"left"},
  {"id":"12" ,"label":"electric company", "price":"£150", "icon":"💡", "color":"none", "order":" 27", "pos":"left"},
  {"id":"11" ,"label":"pall mall", "price":"£140", "icon":"", "color":"pink", "order": "29", "pos":"left"},
  {"id":"31" ,"label":"regent street", "price":"£300", "icon":"", "color":"green", "order": "14", "pos":"right"},
  {"id":"32" ,"label":"oxford street", "price":"£300", "icon":"", "color":"green", "order": "16", "pos":"right"},
  {"id":"33" ,"label":"community chest", "price":"", "icon":"💰", "color":"none", "order": "18", "pos":"right"},
  {"id":"34" ,"label":"bond street", "price":"£320", "icon":"", "color":"green", "order": "20", "pos":"right"},
  {"id":"35" ,"label":"liverpool st. station", "price":"£320", "icon":"🚂", "color":"none", "order": "22", "pos":"right"},
  {"id":"36" ,"label":"chance", "price":"", "icon":"", "color":"none", "order": "24", "pos":"right"},
  {"id":"37" ,"label":"park lane", "price":"£350", "icon":"", "color":"blue", "order": "26", "pos":"right"},
  {"id":"38" ,"label":"super<br />tax", "price":"£100", "icon":"💍", "color":"none", "order": "28", "pos":"right"},
  {"id":"39" ,"label":"mayfair", "price":"£400", "icon":"", "color":"blue", "order": "30", "pos":"right"},
  {"id":"9" ,"label":"pentonville road", "price":"£120", "icon":"", "color":"sky", "order": "32", "pos":"bottom"},
  {"id":"8" ,"label":"euston road", "price":"£100", "icon":"", "color":"sky", "order": "33", "pos":"bottom"},
  {"id":"7" ,"label":"chance", "price":"", "icon":"❓", "color":"none", "order": "34", "pos":"bottom"},
  {"id":"6" ,"label":"the angel, islington", "price":"£100", "icon":"", "color":"sky", "order": "35", "pos":"bottom"},
  {"id":"5" ,"label":"kings cross station", "price":"£200", "icon":"🚂", "color":"none", "order": "36", "pos":"bottom"},
  {"id":"4" ,"label":"income<br />tax", "price":"£200", "icon":"🔸", "color":"none", "order": "37", "pos":"bottom"},
  {"id":"3" ,"label":"whitechapel road", "price":"£60", "icon":"", "color":"brown", "order": "38", "pos":"bottom"},
  {"id":"2" ,"label":"community chest", "price":"", "icon":"💰", "color":"none", "order": "39", "pos":"bottom"},
  {"id":"1" ,"label":"old kent road", "price":"£60", "icon":"", "color":"brown", "order": "40", "pos":"bottom"}
]};

var tiles = "";

for (var t = 0; t < Tiles.List.length; t++){
tiles += "<div id=\"" + Tiles.List[t].id + "\" class=\"" + Tiles.List[t].pos + " " + Tiles.List[t].color + "\" style=\"--order:" + Tiles.List[t].order + ";\"><div class=\"inside\"><h2>" + Tiles.List[t].label + "</h2> <span>" + Tiles.List[t].icon + "</span> <strong>" + Tiles.List[t].price + "</strong></div></div>"
}

$(".frame").append(tiles);



const player = document.createElement('img');
player.src = "/static/img/monopoly_piece_1.svg";
player.id="monopoly-1";
player.className="piece";

document.getElementById("2").appendChild(player);







document.addEventListener("keydown", function (event) {
        // Check the key code of the pressed key
        switch (event.code) {
            case "KeyR":
                socket.emit("roll");

                break;
        }


    });




