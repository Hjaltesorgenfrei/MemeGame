import {setCookie, getCookie, eraseCookie} from "./cookies.js";
import {Card} from "./Card.js";
customElements.define('play-card', Card);

let socket = new WebSocket("wss://mega-meme-game.herokuapp.com/");
// let socket = new WebSocket("ws://localhost:5678");

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

function get_user_id() {
    return getCookie("user_guid") ?? generate_guid();
}

function usernameChanged(username, user_id) {
    if (get_user_id() == user_id) {
        setCookie("username", username, 30);
        show_username.innerHTML = username;
    }
    console.log(`User(${user_id}) changed name to ${username}`);
}

function join_with_username(username) {
    let message = {
        type: 'user_joined',
        username: username,
        user_id: get_user_id()
    };
    socket.send(JSON.stringify(message));
}

// Socket Setup

socket.addEventListener('open', function (event) {
    let saved_username = getCookie("username");
    if (saved_username !== null) {
        join_with_username(saved_username);
    }
});
socket.addEventListener('message', function (event) {
    let data = JSON.parse(event.data);
    switch(data.type) {
        case 'username_change_approve':
            usernameChanged(data.username, data.user_id);
            break;
        case 'game_started':
            setCurrentHost(data.host);
            gameStarted();
            break;
        case 'game_in_progress':
            setCurrentHost(data.host);
            gameStarted();
            break;
        case 'game_ended':
            setCurrentHost("No Game In Progress");
            gameEnded();
            break;
        case 'current_cards':
            createTextCards(data.top_texts, data.bottom_texts);
            break;
        default: 
            console.log("Unhandled data", data);
    }   
});

function saveNameChange() {
    let input = document.getElementById('name_field');
    if (socket.readyState == socket.OPEN) {
        let message = {
            type: 'username_change_request',
            username: input.value,
            user_id: get_user_id()
        };
        socket.send(JSON.stringify(message));
    }
}

function startGame() {
    if (socket.readyState == socket.OPEN) {
        let message = {
            type: 'start_game',
            user_id: get_user_id()
        };
        socket.send(JSON.stringify(message));
    }
}

function endGame() {
    if (socket.readyState == socket.OPEN) {
        let message = {
            type: 'end_game',
            user_id: get_user_id()
        };
        socket.send(JSON.stringify(message));
    }
}

function setCurrentHost(hostname) {
    let current_host = document.getElementById('current_host');
    current_host.innerHTML = hostname;
}

function createTextCards(top_texts, bottom_texts) {
    if (top_texts) {
        let top_texts_container = document.getElementById('top_texts');
        top_texts_container.innerHTML = "";
        top_texts.forEach(element => {
            let card = new Card(element);
            top_texts_container.appendChild(card);
        });
    }
    if (bottom_texts) {
        let bottom_texts_container = document.getElementById('bottom_texts');
        bottom_texts_container.innerHTML = "";
        bottom_texts.forEach(element => {
            let card = new Card(element);
            bottom_texts_container.appendChild(card);
        });
    }
}

function joinedGameInProgress() {

}

function gameStarted() {
    let message = {
        type: 'ask_for_cards',
        user_id: get_user_id()
    };
    socket.send(JSON.stringify(message));
}

function gameEnded() {
    let top_texts = document.getElementById('top_texts');
    top_texts.innerHTML = "";
    let bottom_texts = document.getElementById('bottom_texts');
    bottom_texts.innerHTML = "";
}

function onStartUp() {
    let show_username = document.getElementById('show_username');
    let saved_username = getCookie("username");
    if (saved_username !== null) {
        show_username.innerHTML = saved_username;
    }

    let save_name_change = document.getElementById('save_name_change');
    save_name_change.onclick = saveNameChange;

    let start_game = document.getElementById('start_game');
    start_game.onclick = startGame;

    let end_game = document.getElementById('end_game');
    end_game.onclick = endGame;
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

onStartUp();