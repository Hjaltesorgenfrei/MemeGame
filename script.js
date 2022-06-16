let socket = new WebSocket("ws://localhost:5678");
socket.addEventListener('open', function (event) {
    socket.send('toptexts');
});
socket.addEventListener('message', function (event) {
    let data = JSON.parse(event.data);
    for (const meme in data) {
        document.body.innerHTML += data[meme].value + "<br>"
    }
    console.log('Message from server ');
});

