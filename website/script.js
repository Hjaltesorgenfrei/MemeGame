// let socket = new WebSocket("ws://mega-meme-game.herokuapp.com/");
function setCookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; SameSite=Strict; path=/";
}
function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {   
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}
function makeid(length) {
    var result           = '';
    var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
      result += characters.charAt(Math.floor(Math.random() * 
 charactersLength));
   }
   return result;
}

function generate_guid() {
    let id = makeid(16);
    setCookie("user_guid", id, 30);
    return id;
}

let own_user_id = getCookie("user_guid") ?? generate_guid();

function username_changed(username, user_id) {
    if (own_user_id == user_id) {
        setCookie("username", username, 30);
        show_username.innerHTML = username;
    }
    console.log(`User(${user_id}) changed name to ${username}`)
}


// Socket Setup
let socket = new WebSocket("ws://localhost:5678");
socket.addEventListener('open', function (event) {
    // socket.send('toptexts');
});
socket.addEventListener('message', function (event) {
    let data = JSON.parse(event.data);
    switch(data.type) {
        case 'username_change_approve':
            username_changed(data.username, data.user_id)
        default: 
            console.log("Unhandled data", data);
    }   
});




let show_username = document.getElementById('show_username');
saved_username = getCookie("username");
if (saved_username !== null) {
    show_username.innerHTML = saved_username;
}

function saveNameChange() {
    let input = document.getElementById('name_field');
    username = input.value;
    if (socket.readyState == socket.OPEN) {
        let message = {
            type: 'username_change_request',
            username: username,
            user_id: own_user_id
        };
        socket.send(JSON.stringify(message))
    }
}

async function getAsByteArray(file) {
    return new Uint8Array(await readFile(file));
}

async function submitImage(inputfield) {
    let file = document.getElementById(inputfield).files[0];
    if (file) {
        var reader = new FileReader();
        reader.readAsText(file, "UTF-8");
        reader.onload = function (evt) {
            console.log(evt.target.result);
        }
        reader.onerror = function (evt) {
            console.log(evt);
        }
    }
}