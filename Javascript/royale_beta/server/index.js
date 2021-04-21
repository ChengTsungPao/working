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

var database = {};

io.on("connection", (socket) => {
    console.log("New connection from user !!!");

    socket.on("sendFromClient", (data) => {
        const [name, room, key, posx, posy] = data;

        if(database[room] === undefined){
            database[room] = []
        }

        console.log("Server Get:");
        console.log(data);
        if(key != undefined){
            if(key === "Move"){
                for(var i = 0; i < database[room].length; i++){
                    if(database[room][i][0] == name){
                        database[room][i] = [name, database[room][i][1], posx, posy];
                        break;
                    }
                }
            }else{
                database[room].push([name, key, posx, posy]);
            }
            
        }
        
        console.log("Server Response:");
        console.log(database[room]);
        socket.emit("sendToClient", database[room]);
        socket.broadcast.to(room).emit("sendToClient", database[room]);
        socket.join(room);
        
    });
});

app.use(router);

server.listen(PORT, () => console.log(`Server has started on port ${PORT}`));




