var dimension = 20;
var chanceOfLiveCell = 0;
var timestep = 100;
var table;
var cells;
var track=-1;


$(document).ready(function() {
	table = $('#main');
	initGame();
	cells = table.find('td');
	placeRand();
	playGame();
});

function placeRand() {
	for (var y = 0; y< dimension; y++) {
		for (var x = 0; x< dimension; x++) {
			var cell = getCell(x,y);
			if (Math.random() > chanceOfLiveCell) cell.addClass('alive');
			else { cell.removeClass('alive');}
		}
	}
}

function getCell(x, y) {
	if (x >= dimension) { x = 0; }
	if (y >= dimension) { y = 0; }
	if (x < 0) { x = dimension -1; }
	if (y < 0) { y = dimension -1; }
	return $(cells[y * dimension + x]);
}

function initGame() {
	var trHtml = [];
	for (var y = 0; y< dimension; y++) {
		trHtml.push('<tr>');
		for (var x = 0; x< dimension; x++) {
			trHtml.push('<td> </td>');
		}
		trHtml.push('</tr>');
	}
	trHtml = trHtml.join('');
	table.append($(trHtml));
}

function playGame() {
	playGen();
}

function playGen() {
		$('td').on('click', function() {
		$(this).addClass('clicked');
		for (var y = 0; y< dimension; y++) {
			for (var x = 0; x< dimension; x++) {				
				if (getCell(x, y).hasClass('clicked')) {
					$(this).removeClass('clicked');
					addLiveCells(x,y);
					$(this).css('background-color','#000');				
				}	
			}
		}
	});
	prepGen();
	renderGen();
	
	setTimeout(function() {playGen();}, timestep);
}

function addLiveCells(x, y) {
	
	if (Math.random() < 0.996) {
		
		getCell(x, y-1).addClass('alive'); 

		getCell(x +1, y).addClass('alive'); 
		getCell(x -1, y+1).addClass('alive'); 
		getCell(x, y+1).addClass('alive'); 
		getCell(x+1, y+1).addClass('alive'); 
	} else {
		getCell(x, y+1).addClass('alive'); 

		getCell(x +1, y).addClass('alive'); 
		getCell(x -1, y-1).addClass('alive'); 
		getCell(x, y-1).addClass('alive'); 
		getCell(x+1, y-1).addClass('alive'); 
	}
}

function renderGen() {
	cells.each(function() {
		var cell = $(this);
		cell.removeClass('alive');
		if (cell.attr('isalive') === 'true' ) {
			cell.addClass('alive');
		}
		cell.removeAttr('isalive');
	});
}

function prepGen() {
	var count = 50;
	for (var y = 0; y< dimension; y++) {
		for (var x = 0; x< dimension; x++) {
			var cell = getCell(x, y);
			var neighbors = getLiveNeighborCount(x, y);
			cell.css('background-color', '#BBBBEE');
			cell.attr('isalive', 'false');
			if (isCellAlive(x, y)) {
				if (neighbors === 2 || neighbors === 3) {
					cell.attr('isalive', 'true');
					count++;
					cell.css('background-color', 'rgb(0,'+count+',0)');
					
				} 
			} else if (neighbors === 3) {
				cell.attr('isalive', 'true');
				count++;
				cell.css('background-color', 'rgb(0,'+count+',0)');
			}
		}
	}
}

function getLiveNeighborCount(x, y) {
	var count = 0;
	if (isCellAlive(x - 1, y-1)) {count++;}
	if (isCellAlive(x, y-1)) {count++;}
	if (isCellAlive(x+1, y-1)) {count++;}
	if (isCellAlive(x -1, y)) {count++;}
	if (isCellAlive(x+1, y)) {count++;}
	if (isCellAlive(x -1, y+1)) {count++;}
	if (isCellAlive(x, y+1)) {count++;}
	if (isCellAlive(x+1, y+1)) {count++;}
	return count;
}

function isCellAlive(x, y) {
	return getCell(x, y).attr('class') === 'alive';
}