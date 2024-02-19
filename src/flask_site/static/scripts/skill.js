// const canvas = null;
// const context = null;

// window.onload = function() {
//     canvas = document.getElementById("board");
//     const dimensions = getObjectFitSize(
//         true,
//         canvas.clientWidth,
//         canvas.clientHeight,
//         canvas.width,
//         canvas.height)
    
//     canvas.width = dimensions.width;
//     canvas.height = dimensions.height;

//     context = canvas.getContext("2d");
//     context.scale(1, 1);

//     const img = new Image();
//     img.src = imagesURL+"/dartboard.png";
//     img.onload = () => {
//         context.drawImage(img, 0, 0, canvas.width, canvas.height);
//     }
// };

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

  	const img = new Image();
  	img.src = imagesURL+"/dartboard.png";
  	img.onload = () => {
    	context.drawImage(img, 0, 0, canvas.width, canvas.height);
  	}

  	setInterval(function() {
    	$.ajax({
     		type: "GET",
     		url: "/positions",
     		theContext: context,
     		xDimension: canvas.width,
     		yDimension: canvas.height,
     		success: function(data){
      			if ($(data.position).length > 0) {
					$("#last-hit").text($(data.position)[2]);
					var randomColor = Math.floor(Math.random()*16777215).toString(16);
					$("#last-hit").attr("style", "color: #" + randomColor);
					let [x, y] = realToVirtual(this.xDimension, this.yDimension, $(data.position)[0], $(data.position)[1])
					plotPoint(this.theContext, x, y);
				}
     		}
   		});
  	}, 1000);
});

function plotPoint(context, x, y) {
  	context.fillStyle = '#00FFFF'
  	context.beginPath();
  	context.arc(x, y, 5, 0, 2 * Math.PI, true);
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