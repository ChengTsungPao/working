import io from 'socket.io-client';

// export const URL = `${process.env.REACT_APP_SERVER_URL}:${process.env.REACT_APP_SERVER_PORT}`;
export const URL = "http://localhost:5000/";

export let socket = io(URL);

export var data = {
    "_id": "123",
    "name": "123",
    "room": "25",
    "gameData": []

}