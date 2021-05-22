import { user } from '../../GetData/Restore'
// import io from 'socket.io-client';

// const URL = "140.120.12.162:5000";

// let socket = io(URL);

export function SetupRoom() {
    // socket.emit("SetupRoom", "init");
    // socket.on("SetupRoom", () => {
        
    // });
    user.Room = 100;
    return user.Room;

}
