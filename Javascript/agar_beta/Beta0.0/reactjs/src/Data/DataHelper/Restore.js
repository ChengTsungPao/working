import io from 'socket.io-client';

export const URL = `${process.env.REACT_APP_SERVER_URL}:${process.env.REACT_APP_SERVER_PORT}`;

export let socket = io(URL);

export var data = {
    "_id": null,
    "name": null,
    "room": null,
    "gameData": []

}