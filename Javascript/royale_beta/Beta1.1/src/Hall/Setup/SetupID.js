import { user } from '../GetData/Restore'
// import io from 'socket.io-client';

// const URL = "140.120.12.162:5000";

// let socket = io(URL);

export function SetupID() {
    // socket.emit("SetupID", "init");
    // socket.on("SetupID", () => {
        
    // });
    user.ID = Math.floor(Math.random() * 1000);
    return user.ID;

}
