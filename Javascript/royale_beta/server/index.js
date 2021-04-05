const express = require('express'); 
const socketio = require('socket.io'); 
const http = require('http');   

const router = require('./router');

const app = express();
const server = http.createServer(app);
const io = socketio(server, {
    cors: {
        origin: '*',
    }
});

const PORT = process.env.PORT || 5000

var data = [];

io.on("connection", (socket) => {
    console.log("New connection from user !!!");

    socket.on("sendFromClient", (message) => {
        console.log(`Server Get: ${message}`);
        data.push(message);

        console.log(`Server Response: ${message}`);
        socket.emit("sendToClient", message);

    });
});

app.use(router);

server.listen(PORT, () => console.log(`Server has started on port ${PORT}`));




