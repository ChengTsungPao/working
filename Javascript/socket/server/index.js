const express = require('express');      // import Express Server API
const socketio = require('socket.io');   // import the socket API
const http = require('http');            // import the http API

const { addUser, removeUser, getUser, getUsersInRoom } = require('./users.js'); // import function

const PORT = process.env.PORT || 5000 // setup port number

const router = require('./router'); // Use Router to conversation with database

const app = express();                 // Build Express Server
const server = http.createServer(app); // Create the socket API
const io = socketio(server, {          // Create http to the connection
  cors: {
    origin: '*',
  }
});

io.on('connection', (socket) => { // Running when the user access
    console.log("We have a new connection!!!"); 

    socket.on('join', ({ name, room }, callback) => { // listening socket (when socket emit Running)
    	const { error, user } = addUser({ id: socket.id, name, room });
    	
        if(error) return callback(error);

        socket.emit('message', { user: 'admin', text: `${user.name}, welcome to the room ${user.room}` }); // call the socket Running
        socket.broadcast.to(user.room).emit('message', { user: 'admin', text: `${user.name}, has joined!` }); // call the socket Running (room === user.room)

        socket.join(user.room);

        io.to(user.room).emit('roomData', { room: user.room, users: getUsersInRoom(user.room)}); // call the socket Running

        callback();
    });

    socket.on('sendMessage', (message, callback) => {
        const user = getUser(socket.id);

        io.to(user.room).emit('message', { user: user.name, text: message });
        io.to(user.room).emit('roomData', { room: user.room, users: getUsersInRoom(user.room)});

        callback();
    });

    socket.on('disconnect', () => {
        const user = removeUser(socket.id);
        console.log(`${user.name} has left.`);
        
        if(user){
          io.to(user.room).emit('message', { user: 'admin', text: `${user.name} has left.` });
        }
    });
});

app.use(router); // when app receive access Running Router

server.listen(PORT, () => console.log(`Server has started on port ${PORT}`)); // server.listen(PORT, callback)