import io from 'socket.io-client';
import { useState, useEffect } from 'react';
import Factory from '../Factory/Factory'

const URL = "localhost:5000";

let socket = io(URL);
var getDataTemp = [];

const Send = () => {
    const [data, setData] = useState([]);
    const [getData, setGetData] = useState([]);

    useEffect(() => {
        console.log("Client Send:");
        console.log(data);
        socket.emit("sendFromClient", data);

    }, [data]);

    useEffect(() => {
        getDataTemp = getData;
    }, [getData]);

    useEffect(() => {
        window.addEventListener('keyup', function(event){
            setData([event.key, getDataTemp.length, getDataTemp.length]);
            // console.log("addEventListener");
            // console.log(getDataTemp);
        });

        socket.on("sendToClient", (data) => {
            console.log("Client Get:");
            console.log(data)
            setGetData(data);
        });
        
    }, [])

    return (
        <div id = "send">
            {data}
            {getData.map((user, index) => {
                return <Factory key = {index} component = {user[0]}/>
            })}
        </div>
    )


}

export default Send;