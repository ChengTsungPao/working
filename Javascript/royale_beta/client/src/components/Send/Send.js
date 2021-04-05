import io from 'socket.io-client';
import { useState } from 'react';

const URL = "localhost:5000";

let socket = io(URL);

const Send = () => {
    const [data, setData] = useState("嗨嗨我是Josh");
    const [sendData, setSendData] = useState("");

    socket.on("sendToClient", (message) => {
        console.log(`Client Get: ${message}`);
        setData(message);
        setSendData("");

    });

    const buttonHandler = () => {
        if(sendData !== ""){
            socket.emit("sendFromClient", sendData);
        }

    }

    return (
        <div>
            <h1>{data}</h1>
            <input onChange  = {(event => setSendData(event.target.value))}/>
            <button onClick = {buttonHandler}>Send</button>
        </div>
    )


}

export default Send;