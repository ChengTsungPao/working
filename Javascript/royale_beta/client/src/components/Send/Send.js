import io from 'socket.io-client';
import { useState, useEffect } from 'react';
import queryString from 'query-string';
import Factory from '../Factory/Factory'
import Keyboard from './Keyboard'
import { Move, GetPosition } from './Move'

const URL = "localhost:5000";

let socket = io(URL);

const Send = ({ location }) => {
    const [data, setData] = useState([]);
    const [getData, setGetData] = useState([]);
    const { name, room } = queryString.parse(location.search);

    useEffect(() => {
        console.log("Client Send:");
        console.log(data);
        socket.emit("sendFromClient", data);

    }, [data]);

    useEffect(() => {
        window.addEventListener('keydown', function(event){
            if(Keyboard('keydown', event.key) && document.getElementById(name) != null){
                Move(name, event.key, 5);
                setData([name, room, "Move", GetPosition(name)[0], GetPosition(name)[1]]);
                // console.log("addEventListener");
                // console.log(getDataTemp);
            }
        });

        window.addEventListener('keyup', function(event){
            if(Keyboard('keyup', event.key)){
                setData([name, room, event.key, Math.floor(Math.random() * 1000) + 50, Math.floor(Math.random() * 500)]);
                // console.log("addEventListener");
                // console.log(getDataTemp);
            }
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
            {getData.map((data, index) => {
                return <Factory key = {index} data = {data} component = {data[2]}/>
            })}
        </div>
    )


}

export default Send;