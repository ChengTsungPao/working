import { map } from '../GetData/Restore'
// import io from 'socket.io-client';

// const URL = "140.120.12.162:5000";

// let socket = io(URL);

export function SetupMap() {
    // socket.emit("SetupMap", "init");
    // socket.on("SetupMap", () => {
        
    // });
    map.kind = "Normal";
    map.data = null;
    return map;

}