//tesseraction.net - copyright 2022 - clayton baber - all rights reserved

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const color_state = ["#333333","red","orange","yellow","green","blue","cyan","purple","#ffffff"];

var cHeight=640;
var cellSize=cHeight/29;

//all positions are relative to a 32x30 grid on the canvas
//first 0:15 pairs represent board posistions. 15:22 player one starting positions, 22:29 player two.
const positions = [[14,1],[9,4],[19,4],[14,7],[9,10],[19,10],[4,13],[14,13],[24,13],[9,16],[19,16],[14,19],[9,22],[19,22],[14,25],[4,4],[3,7],[2,10],[1,13],[2,16],[3,19],[4,22],[24,4],[25,7],[26,10],[27,13],[26,16],[25,19],[24,22]];

//lines connecting board positions
const lines = [[0,1],[0,2],[0,4],[0,5],[1,6],[1,7],[1,3],[2,3],[2,7],[2,8],[3,9],[3,10],[4,6],[4,7],[4,11],[5,7],[5,8],[5,11],[6,12],[6,9],[7,9],[7,10],[7,12],[7,13],[8,10],[8,13],[9,14],[10,14],[11,12],[11,13],[12,14],[13,14]];

//index here represents a board position, the value represent board positions that are neighbors
const neighbors = [[1,2,4,5],[0,3,6,7],[0,3,7,8],[1,2,9,10],[0,6,7,11],[0,7,8,11],[1,4,9,12],[1,2,4,5,9,10,12,13],[2,5,10,13],[3,6,7,14],[3,7,8,14],[4,5,12,13],[6,7,11,14],[7,8,11,14],[9,10,12,13]];

//t_space defines how a piece will be isomorphically transformed when it arrives at this position
const t_space = [0,0,0,1,4,6,0,2,0,7,5,3,0,0,0]

//this indicates who is occupying a positions
//first 15 elements represent the positions on the board.
//the next 7 are player one starting positions;
//the next 7, player two.
//each position hold 4 values. the sum of their values determines who owns the piece (as well as the color). positive: player one. negative: player two. zero: both.
var occupations = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[1,1,1,0],[1,1,1,-1],[1,0,0,1],[1,1,0,0],[1,-1,0,1],[1,1,-1,0],[1,0,0,0],[-1,-1,-1,0],[-1,-1,-1,1],[-1,0,0,-1],[-1,-1,0,0],[-1,1,0,-1],[-1,-1,1,0],[-1,0,0,0]];

//the selected list represents which piece has been selected to be moved... should only have one nonzero value at a time, sometimes none
var selected = new Array(29);
selected.fill(0);


//this contains all pertinent drawing locations for board stuff (positions, lines)
//should be recalculated each time the playing surface changes size
var pixels = new Array(75);
pixels.fill([0,0,0,0]);

var expected_play = [1,0];
var turn = 1;

function calculate_pixels(size){
	
	cHeight=size;
    cellSize = cHeight / 29;

    //positions
    for(var i=0; i<29; i++){
        pixels[i] = [positions[i][0]*cellSize+cellSize/4, positions[i][1]*cellSize+cellSize/4, (positions[i][0]+1)*cellSize-cellSize/4, (positions[i][1]+1)*cellSize-cellSize/4];
	}
	
    //lines
    for(var i=0; i <32; i++){
        pixels[i+29] = [positions[lines[i][0]][0]*cellSize+(cellSize/2), positions[lines[i][0]][1]*cellSize+(cellSize/2),positions[lines[i][1]][0]*cellSize+(cellSize/2), positions[lines[i][1]][1]*cellSize+(cellSize/2)];
	}
	
    //misc
    pixels[74] = [cellSize/4, cellSize/8, cellSize, cellSize/2];

    draw();
}

function draw_t_space(posx, posy, transformer){
    if(transformer == 0){
        return
    }
	
    const number = cellSize/2;
    const number2 = cellSize/3;
    const number3 = cellSize/2.5;
    const number4 = cellSize/12;
    const number5 = cellSize/4;
    
    if(transformer == 1){
        create_arc(posx - number3, posy - number3, posx + number3, posy + number3, 0, 180, number4, false);
    } else if(transformer == 2){
        create_arc(posx - number5, posy - number5*2 -1, posx + number5, posy, 85, 210, number4, true);
        create_arc(posx - number5 -0.5, posy + 0.5, posx + number5 +1, posy + number5*2, 40, 275, number4, false);
    } else if(transformer == 3){
        create_arc(posx - number3, posy - number3, posx + number3, posy + number3, 0, 180, number4, true);
    } else if(transformer == 4){
       create_line(posx, posy - number, posx, posy + number, "black", number4);
    } else if(transformer == 5){
        create_line(posx - number, posy, posx + number, posy, "black",number4);
    } else if(transformer == 6){
        create_line(posx - number2, posy + number2, posx + number2, posy - number2, "black", number4);
    } else if(transformer == 7){
        create_line(posx - number2, posy - number2, posx + number2, posy + number2, "black", number4);
	}
}

function draw_st(posx, posy, state){
    var color = color_state[4+state[0]+state[1]+state[2]+state[3]];
    const number = cellSize/2;
    const number2 = number * 1.75;
    const number3 = number / 4;
    const number4 = number/6;
	const number5 = number + 5;
    create_rectangle(posx - number, posy - number, number*2, number*2, "black", color, number4);
    
    //draw the four statelettes
    if(state[0] != 0){
        if(state[0] == 1){
            color = "white";
		} else{
            color = color_state[0];
		}
        create_oval(posx - number2, posy - number2, posx - number3, posy - number3, "black", color, number4);
    }
	
	if(state[1] != 0){
        if(state[1] == 1){
            color = "white";
        } else {
            color = color_state[0];
		}
        create_oval(posx + number3, posy - number2, posx + number2, posy - number3, "black", color, number4);
	}

    if(state[2] != 0){
        if(state[2] == 1){
            color = "white";
        } else {
            color = color_state[0];
		}
		create_oval(posx - number2, posy + number2 + number5, posx - number3, posy + number3 + number5, "black", color, number4);
	}

    if(state[3] != 0){
        if(state[3] == 1){
            color = "white";
        } else {
            color = color_state[0];
		}
        create_oval(posx + number3, posy + number2 + number5,posx + number2, posy + number3 + number5, "black", color, number4);
	}
}

function create_circle(x, y, r, w, color){
	ctx.beginPath();
	ctx.lineWidth = w;
	ctx.strokeStyle = color;
	ctx.arc(x, y, r, 0, 6.28);
	ctx.stroke();
}

function create_rectangle(x1, y1, x2, y2, outline, fill, width){
	ctx.beginPath();
	ctx.strokeStyle = outline;
	ctx.lineWidth = width;
	ctx.fillStyle = fill;
	ctx.rect(x1, y1, x2, y2);
	ctx.stroke();
	if(fill !== false){
		ctx.fill();
	}
}

function create_arc(x1, y1, x2, y2, start, end, width, clockwise){
	const rx = (x2 - x1)/2;
	const ry = (y2 - y1)/2;
	const x = x2 - rx;
	const y = y2 - ry;
	
	ctx.beginPath();
	ctx.strokeStyle = "black";
	ctx.lineWidth = width;
	ctx.arc(x, y, rx, start * 0.0174, end * 0.0174, clockwise);
	ctx.stroke();
	
}

function create_line(x1, y1, x2, y2, color, width){
	ctx.strokeStyle = color;
	ctx.lineWidth = width;
	ctx.beginPath();
	ctx.moveTo(x1, y1);
	ctx.lineTo(x2, y2);
	ctx.stroke();
}

function create_oval(x1, y1, x2, y2, outline, fill, width){

	const rx = Math.abs((x2 - x1)/2);
	const ry = Math.abs((y2 - y1)/2);
	const x = x2 - rx;
	const y = y2 - ry;

	ctx.beginPath();
	ctx.strokeStyle = outline;
	if(fill !== false){
		ctx.fillStyle = fill;
	}
	ctx.lineWidth = width;
	ctx.moveTo(x, y);
	ctx.ellipse(x, y, rx, ry, 0, 0, 6.28);
	ctx.stroke();
	if(fill !== false){
		ctx.fill();
	}
}


//this function will draw the current gamestate on the canvas.
function draw(){

    //wipe the canvas clean
	ctx.fillStyle = "#424242";
    ctx.fillRect(0, 0, cHeight, cHeight);
    var color = "#adadad";

   //draw the connecting lines
    for(var i=29; i<61; i++){
		create_line(pixels[i][0], pixels[i][1], pixels[i][2], pixels[i][3], color, pixels[74][0]);
	}
	
	//draw each of the board positions
	for(var i=0; i < 15; i++){
        create_oval(pixels[i][0], pixels[i][1], pixels[i][2], pixels[i][3], color, color, pixels[74][2]);
        draw_t_space(pixels[i][0]+pixels[74][0], pixels[i][1]+pixels[74][0], t_space[i]);
	}
	
	//draw a player piece on the position it is occupying
    for(var i=0; i<29; i++){
	    if(!occupations[i].every((v,i)=>v==0)){
            draw_st(pixels[i][0]+pixels[74][0], pixels[i][1]+pixels[74][0], occupations[i]);
		}
    }
	
	//turn has 3 distinct positbilities due to output rounding
    if(turn == 1){
		color = "white";
	} else if(turn == 0) {
		color = "#adadad";
	} else {
		color = "black";
	}
	
	//draw which positions are selected
	for(var i=0; i < selected.length; i++){
		if(selected[i] == 1){
			create_circle(pixels[i][0]+pixels[74][2]/4, pixels[i][1]+pixels[74][2]/4, pixels[74][2]*1.25, pixels[74][1], color);
		}
		if(selected[i] == -1){
			
			create_rectangle(pixels[i][0]-cellSize, pixels[i][1]-cellSize, cellSize*2.5,  cellSize*2.5, color, false, pixels[74][1]);
		}
	}
	
	//draw who's turn it is
	create_circle(0,0,cellSize*2, cellSize, color);
	create_circle(0,cHeight,cellSize*2, cellSize, color);
	create_circle(cHeight,0,cellSize*2, cellSize, color);
	create_circle(cHeight,cHeight,cellSize*2, cellSize, color);
	
	//normally expected_play should only be either [1,0] or [0,1]
	//but can also be in the strange states of [0,-1], [-1,-1], [-1,0], or [1,1]
	
	//draw expected_play[0]
	if(expected_play[0] == -1){
		create_circle(0,0,cellSize/2, cellSize/4, color);
		create_circle(0,cHeight,cellSize/2, cellSize/4, color);
		create_circle(cHeight,0,cellSize/2, cellSize/4, color);
		create_circle(cHeight,cHeight,cellSize/2, cellSize/4, color);
	} else if(expected_play[0] == 1){
		create_circle(0,0,cellSize, cellSize/4, color);
		create_circle(0,cHeight,cellSize, cellSize/4, color);
		create_circle(cHeight,0,cellSize, cellSize/4, color);
		create_circle(cHeight,cHeight,cellSize, cellSize/4, color);
	}
	
	//draw expected_play[1]
	if(expected_play[1] == -1){
		create_circle(0,0,cellSize*3.5, cellSize/4, color);
		create_circle(0,cHeight,cellSize*3.5, cellSize/4, color);
		create_circle(cHeight,0,cellSize*3.5, cellSize/4, color);
		create_circle(cHeight,cHeight,cellSize*3.5, cellSize/4, color);
	} else if(expected_play[1] == 1){
		create_circle(0,0,cellSize*3, cellSize/4, color);
		create_circle(0,cHeight,cellSize*3, cellSize/4, color);
		create_circle(cHeight,0,cellSize*3, cellSize/4, color);
		create_circle(cHeight,cHeight,cellSize*3, cellSize/4, color);
	}
}

//loop through the positions and see if mouse click was on a board position
function click(event){
	const finger = cellSize;
	for(var i=0; i < 29; i++){
        if(event.x > pixels[i][0]-finger && event.x < pixels[i][2]+finger && event.y > pixels[i][1]-finger && event.y < pixels[i][3]+finger){
            //clicked registered on the i'th position, process it
            clicked(i);
            break;
		}
	}
}

function clicked(value){
	
	waiting = true;
	
	var action = new Array(29);
	action.fill(0);
	action[value] = 1;
	
		//build our request from the turn expected_play occupations selected action
	var request = new Array();
	request.push(turn,expected_play,occupations.flat(),selected,action);
	request = request.flat();
		
	//change the world
	update(request).then((result)=>{
		
		var gamestate = new Array();
		result.map((element)=>{
			gamestate.push(Math.round(element));
		});
		
		turn = gamestate[0]
		
		expected_play = gamestate.slice(1, 3);
		
		selected = gamestate.slice(119,148);
		
		var occuspot = 0;
		var occuslice = gamestate.slice(3,119);
		for(var i = 0; i < occuslice.length; i+=4){
			
			occupations[occuspot] = [occuslice[i], occuslice[i+1], occuslice[i+2], occuslice[i+3]];
			occuspot++;
		}
		
		
		
		//we've made changes to the gamestate, so lets update board view
		draw();
		waiting = false;
	});
}

async function update(request) {
  // Get the predictions for the canvas data.co

  const input = new onnx.Tensor(request, "float32", [1,177]);

  const outputMap = await sess.run([input]);
  const outputTensor = outputMap.values().next().value;
  const prediction = outputTensor.data;
  
  return prediction;
}

function canvasMouseDown(event) {

	const x = event.offsetX;
	const y = event.offsetY;
	click({x:x,y:y});
}

// Load our model.
const sess = new onnx.InferenceSession();
const loadingModelPromise = sess.loadModel("tesseraction.onnx");

function resizeCanvas(){
	const width = window.innerWidth;
	const height = window.innerHeight;
	const size = Math.min(width, height) - 38;
	
	canvas.width = size;
	canvas.height = size;
	calculate_pixels(size);
}

loadingModelPromise.then(() => {
	resizeCanvas();
	window.addEventListener("resize", resizeCanvas);
	canvas.addEventListener("mousedown", canvasMouseDown);
})
