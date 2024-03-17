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
    	$.ajax({
     		type: "GET",
     		url: "/scores",
			theContext: context,
     		xDimension: canvas.width,
     		yDimension: canvas.height,
     		success: function(data){
				$("#a1").text($(data.scores)[0][0]);
				$("#a2").text($(data.scores)[0][1]);
				$("#a3").text($(data.scores)[0][2]);
				$("#b1").text($(data.scores)[1][0]);
				$("#b2").text($(data.scores)[1][1]);
				$("#b3").text($(data.scores)[1][2]);

				$("#atotal").text($(data.totals)[0]);
				$("#btotal").text($(data.totals)[1]);

				if (data.change == true) {
					$(".player").toggleClass("active");
				}

				if (data.just_won == true) {
					$("#a_wins").text($(data.wins)[0]);
					$("#b_wins").text($(data.wins)[1]);

					element = $(".left");
					playerA = element.children(":first");
					if (data.active_player == 0) {
						playerA.addClass("active");
						playerA.next().removeClass("active");
					}
					else {
						playerA.removeClass("active");
						playerA.next().addClass("active");
					}
				}

				if (data.clear == true) {
					this.theContext.clearRect(0, 0, this.xDimension, this.yDimension);
				}
				
				if ($(data.position).length > 0) {
					let [x, y] = realToVirtual(this.xDimension, this.yDimension, $(data.position)[0], $(data.position)[1])
					plotPoint(this.theContext, x, y);
				}
     		}
   		});
  	}, 1000);
});

function plotPoint(context, x, y) {
  	context.fillStyle = '#6495ED';
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