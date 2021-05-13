// import { CollisionEvent, MoveCollision } from './components/Collision/CollisionEvent.js';

const Collision = require('./components/Collision/CollisionEvent');
const collision = new Collision();

const express = require('express'); 
const socketio = require('socket.io'); 
const http = require('http');   

const router = require('./router');
const { CLIENT_RENEG_LIMIT } = require('tls');

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
        
        const collisionResult = collision.CollisionCircleEvent(name, [posx, posy], database[room], 12)
        collision.CollisionRectEvent(name, [posx, posy], database[room], 12)
        if(collisionResult.event){
            console.log("collision");
            const move = collision.MoveCollision([posx, posy], [database[room][collisionResult.index][2], database[room][collisionResult.index][3]], 5);
            database[room][collisionResult.index][2] += move[0];
            database[room][collisionResult.index][3] += move[1];

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




