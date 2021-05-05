import io from 'socket.io-client';
import { useState, useEffect } from 'react';
import queryString from 'query-string';
import Factory from '../Factory/Factory'
import Keyboard from './Keyboard'
import { Move, GetPosition, MoveCollision } from './Move'
import { CollisionEvent } from './Collision'

const URL = "localhost:5000";

let socket = io(URL);
var getDataTemp = [];

const Send = ({ location }) => {
    const [getData, setGetData] = useState([]);
    const { name, room } = queryString.parse(location.search);

    const sendData = (data) => {
        console.log("Client Send:");
        console.log(data);
        socket.emit("sendFromClient", data);
    }

    useEffect(() => {
        getDataTemp = getData
    }, [getData])

    useEffect(() => {
        window.addEventListener('keydown', function(event){
            if(Keyboard('keydown', event.key) && document.getElementById(name) != null){
                
                // console.log(getDataTemp)
                const collision = CollisionEvent(name, GetPosition(name), getDataTemp, 12)
                if(collision.event){
                    const vector = MoveCollision(GetPosition(name), GetPosition(collision.name), 5)
                    sendData([[collision.name, room, "Move", GetPosition(collision.name)[0] + vector[0], GetPosition(collision.name)[1] + vector[1]], 
                              [name, room, "Move", GetPosition(name)[0] + Move(event.key, 5)[0], GetPosition(name)[1] + Move(event.key, 5)[1]]]);
                }else{
                    sendData([[name, room, "Move", GetPosition(name)[0] + Move(event.key, 5)[0], GetPosition(name)[1] + Move(event.key, 5)[1]]]);
                }
            }
        });

        window.addEventListener('keyup', function(event){
            if(Keyboard('keyup', event.key)){
                sendData([[name, room, event.key, Math.floor(Math.random() * 1000) + 50, Math.floor(Math.random() * 500)]]);
            }
        });

        socket.on("sendToClient", (data) => {
            console.log("Client Get:");
            console.log(data)
            setGetData(data);
        });

        sendData([[name, room]]);
        
        // eslint-disable-next-line
    }, [])

    return (
        <div id = "send">
            {getData.map((data, index) => {
                return <Factory key = {index} data = {data} component = {data[1]}/>
            })}
        </div>
    )


}

export default Send;