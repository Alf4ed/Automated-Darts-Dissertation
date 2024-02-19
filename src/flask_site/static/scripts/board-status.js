function changeMode(data) {
    $.ajax({
        type: "PUT",
        url: "/changeMode/"+data,
    });
};

function moveCam(camID, direction) {
    $.ajax({
        type: "PUT",
        url: "/moveCam/"+camID+"/"+direction,
    });
};

function updateThresh() {
    $.ajax({
        type: "PUT",
        url: "/updateThresh/"+$('#threshold').val(),
    });
}

function centerLine() {
    $.ajax({
        type: "PUT",
        url: "/centerLine/"+$('#showCenter').is(":checked"),
    });
}