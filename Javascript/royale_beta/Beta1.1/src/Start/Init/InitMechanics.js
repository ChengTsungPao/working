import { GetData } from '../../Hall/GetData/GetData'
// import io from 'socket.io-client';

// const URL = "140.120.12.162:5000";

// let socket = io(URL);

export function InitMechanics() {
    // socket.emit("InitMechanics", "init");
    // socket.on("InitMechanics", () => {
        
    // });
    const map = GetData("map");
    const mechanics = {r: [Math.floor(Math.random() * map.size), Math.floor(Math.random() * map.size)], 
                       v: 0, 
                       a: 0}
    return mechanics;

}
