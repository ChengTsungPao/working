import { map } from '../../GetData/Restore'
// import io from 'socket.io-client';

// const URL = "140.120.12.162:5000";

// let socket = io(URL);

export function SetupMap() {
    // socket.emit("SetupMap", "init");
    // socket.on("SetupMap", () => {
        
    // });
    map.kind = "Normal";
    map.size = [5000, 5000];
    map.data = null;
    return map;

}