let skilling = false;

$(document).ready(function() {
	const canvas = document.getElementById("board");
  	const dimensions = getObjectFitSize(
    	true,
    	canvas.clientWidth,
    	canvas.clientHeight,
    	canvas.width,
    	canvas.height)
    
  	canvas.width = dimensions.width;
  	canvas.height = dimensions.height;

  	const context = canvas.getContext("2d");
  	context.scale(1, 1);

	// blur effect
	context.shadowBlur = 10;
	context.shadowColor = '#6495ED';

	$('#board').css('background-image', 'url('+imagesURL+'/dartboard.png'+')');
	$('#board').css('background-size', 'contain');
	$('#board').css('background-repeat', 'no-repeat');
	$('#board').css('background-position', 'center');

	setInterval(function() {
		if (skilling) {
			$.ajax({
				type: "GET",
				url: "/positions",
				theContext: context,
				xDimension: canvas.width,
				yDimension: canvas.height,
				success: function(data){
					if ($(data.position).length > 0) {
						$("#last-hit").text(data.score);
						let [x, y] = realToVirtual(this.xDimension, this.yDimension, $(data.position)[0], $(data.position)[1])
						plotPoint(this.theContext, x, y);
					}
				}
			});
		}
	}, 1000);
});

function startSkill() {
	let person = prompt("What is your name?")
	$.ajax({
        type: "PUT",
        url: "/start-skill",
		contentType: "application/json",
		data: JSON.stringify({ name: person }),
    });
	skilling = true;
}

function stopSkill() {
	skilling = false;
	alert("Skill calculation is over.")
	$.ajax({
        type: "PUT",
        url: "/stop-skill",
    });
}

function plotPoint(context, x, y) {
  	context.fillStyle = '#6495ED'
  	context.beginPath();
  	context.arc(x, y, 7, 0, 2 * Math.PI, true);
  	context.fill();
	context.fillStyle = 'Black';
  	context.beginPath();
  	context.arc(x, y, 3, 0, 2 * Math.PI, true);
  	context.fill();
}

function realToVirtual(width, height, xCoord, yCoord) {
	let transX = width*(xCoord + 200)/460 + 3*width/46;
	let transY = height*(-yCoord + 200)/460 + 3*height/46;

  	return [transX, transY]
}

// adapted from: https://www.npmjs.com/package/intrinsic-scale
function getObjectFitSize(
    contains /* true = contain, false = cover */,
    containerWidth,
    containerHeight,
    width,
    height) {
    var doRatio = width / height;
    var cRatio = containerWidth / containerHeight;
    var targetWidth = 0;
    var targetHeight = 0;
    var test = contains ? doRatio > cRatio : doRatio < cRatio;
  
    if (test) {
      targetWidth = containerWidth;
      targetHeight = targetWidth / doRatio;
    } else {
      targetHeight = containerHeight;
      targetWidth = targetHeight * doRatio;
    }
  
    return {
      width: targetWidth,
      height: targetHeight,
      x: (containerWidth - targetWidth) / 2,
      y: (containerHeight - targetHeight) / 2
    };
  }