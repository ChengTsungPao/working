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

var database = [];

io.on("connection", (socket) => {
    console.log("New connection from user !!!");

    socket.on("sendFromClient", (data) => {
        console.log("Server Get:");
        console.log(data);
        if(data.length >= 1){
            database.push(data);
        }
        
        console.log("Server Response:");
        console.log(database);
        socket.emit("sendToClient", database);

    });
});

app.use(router);

server.listen(PORT, () => console.log(`Server has started on port ${PORT}`));




