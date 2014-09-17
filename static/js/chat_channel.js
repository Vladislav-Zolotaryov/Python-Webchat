var interval;
var pathname = window.location.pathname;

$( document ).ready(function() {
    interval = setInterval(updateStatus, 500);
});

function updateStatus() {
    $.ajax({
        type: "POST",
        url: pathname + "/status"
    }).done(function(msg) {
        usersHtml = '';
        $.each(msg.users, function() {
             usersHtml += $.parseJSON(this).name + '<BR>';
        });
        $('.chat-channel-users-block').html(usersHtml);
        
        messagesHtml = '';
        $.each(msg.messages, function() {
            var item = $.parseJSON(this);
             messagesHtml += '['+ item.timestamp +'] ' + item.username + ': ' + item.message + '<BR>';
        });
        $('.chat-channel-messages-block').html(messagesHtml);
    });
}   

function sendMessage() {
    var pathname = window.location.pathname;
    var message =  $('#messageBox').val();
    $('#messageBox').val('');
    $.ajax({
        type: "POST",
        url: pathname + "/post_message", data: {'message' : message}
    });
}    