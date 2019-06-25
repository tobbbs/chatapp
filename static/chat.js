$(document).ready(function() {
    function fetch() {
        $.get("/chatroom", function(get_messages) {
            $("#new_messages").html("")
            var messages = JSON.parse(get_messages)
            messages.forEach(function(x){
                var name = x[0];
                var message = x[1];
                $("#new_messages").append(`<p><span class="username">${name}</span>:<span>${message}</span></p>`);
            });  
            var objDiv = document.getElementById("new_messages");
            objDiv.scrollTop = objDiv.scrollHeight;    
        });
    }

    $("#submit").click(function(e) {
        e.preventDefault();
        var inputMessage = $("#input_message").val();
        $("#input_message").val("");
        $("#input_message").focus()
        console.log(inputMessage);
        $.post("/chatroom", {message: inputMessage}, function(post_messages) {
            var message = JSON.parse(post_messages)
            $("#new_messages").append(`<p>${message}</p>`);
        });
    });

    $("#target").click(function() {
        $.get("/random", function(data) {
            $("#random-string").append(`<p>${data}</p>`);
        });
    });
    if element.scroll()
    setInterval(function(){ fetch(); }, 500);
});