window.onload = function() {
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
};

// adapted from: https://www.npmjs.com/package/intrinsic-scale
function getObjectFitSize(
    contains /* true = contain, false = cover */,
    containerWidth,
    containerHeight,
    width,
    height
  ) {
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