function centerLine() {
    $.ajax({
        type: "PUT",
        url: "/centerLine/"+$('#showCenter').is(":checked"),
    });
}