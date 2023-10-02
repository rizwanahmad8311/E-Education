// chat.js
$(document).ready(function() {
    // Function to scroll to the bottom of the chat container
    function scrollToBottom() {
        var chatContent = document.getElementById('chat-content');
        chatContent.scrollTop = chatContent.scrollHeight;
    }

    // Call the scrollToBottom function initially to scroll to the bottom
    scrollToBottom();

   



// WebSocket
const groupname = JSON.parse(document.getElementById('group-name').textContent)

// var ws = new WebSocket('ws://127.0.0.1:8000/ws/sc/')

var ws = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/ac/'
    + groupname
    + '/'
    )
    
    ws.onopen = function(){
        // const chatbox = document.getElementById('#chatbox')
        // chatbox.scrollTop = chatbox.scrollHeight
        console.log("websocket connection open...",groupname)

    }
    ws.onmessage = function(event){
        // console.log("Message Received from server...",event.data)
        const data = JSON.parse(event.data)      //  string to object
        const currentUser = JSON.parse(document.getElementById('user_name').textContent);
        const first_name = JSON.parse(document.getElementById('first_name').textContent);
        const last_name = JSON.parse(document.getElementById('last_name').textContent);
        var date = new Date();
        var hours = date.getHours();
        var hours = date.getHours();
        var minutes = date.getMinutes();
        var ampm = hours >= 12 ? 'p.m.' : 'a.m.';
        hours = hours % 12;
        hours = hours ? hours : 12; // the hour '0' should be '12'
        minutes = minutes < 10 ? '0'+minutes : minutes;
        var strTime = hours + ':' + minutes + ' ' + ampm;

        
        var strDate = (date.toLocaleString('en-US', { month: 'long' })).slice(0, 3)+'. '  + date.getDate()+', ' + date.getFullYear() + ', '
        if (data.user==currentUser){
            // console.log(first_name);
            
            // let userHtml = '<p class="userText"><span>' + data.msg  + '</span></p>';

            let userHtml ='<div class="media media-chat media-chat-reverse">'+
            '<div class="media-body">'+
            '<p> <span class="text-dark"><u>'+ first_name + ' ' + last_name +'</u></span> <br>'+ data.msg +'</p>'+
            '<p class="meta text-dark"><time datetime="2018">'+ strDate + strTime+ '</time></p>'+
            '</div>'+
            '</div>'
            
            $("#chat-content").append(userHtml);
            scrollToBottom();
            
        }else{
            // console.log(first_name);
            let userHtml ='<div class="media media-chat">'+
            '<div class="media-body">'+
            '<p> <span class="text-dark"><u>'+ data.f_name + ' ' + data.l_name +'</u></span> <br>'+ data.msg +'</p>'+
                '<p class="meta"><time datetime="2018">'+strDate + strTime + '</time></p>'+
            '</div>'+
        '</div>'

            $("#chat-content").append(userHtml);
            scrollToBottom();
        }
                

}
ws.onerror = function(event){
console.log("websocket error occurred...",event)
}
ws.onclose = function(event){
console.log("websocket connection closed ...",event)
}





//Gets the text text from the input box and processes it
function getResponse() {
    let userText = $("#textInput").val();
    if (userText ==''){
    }
    else{

        $("#textInput").val("");
        ws.send(JSON.stringify({
            'msg':userText
        }))
    }


}


function sendButton() {
    getResponse();
}


// Press enter to send a message
$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        getResponse();
    }
});


});