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
        // const room = data[1];

        console.log("Server Get:");
        console.log(data);
        if(data.length >= 1){
            if(data[2] != "Move"){
                database.push(data);
            }else{
                for(var i = 0; i < database.length; i++){
                    if(database[i][0] == data[0] && database[i][1] == data[1]){
                        database[i][3] = data[3];
                        database[i][4] = data[4];
                        break;
                    }
                }
            }
            
        }
        
        console.log("Server Response:");
        console.log(database);
        // socket.broadcast.to(room).emit("sendToClient", database);
        // socket.join(room);
        socket.emit("sendToClient", database);

    });
});

app.use(router);

server.listen(PORT, () => console.log(`Server has started on port ${PORT}`));




