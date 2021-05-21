import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Login = () => {
    const [name, setName] = useState("");
    const [room, setRoom] = useState("");


    return (
        <div>
            <div>
                <h1>Login</h1>
                <div><input placeholder = "Name" type = "text" onChange = {(event) => setName(event.target.value)}/></div>
                <div><input placeholder = "Room" type = "text" onChange = {(event) => setRoom(event.target.value)}/></div>
                <Link onClick = {event => (!name || !room) ? event.preventDefault() : null} to = {`/Send?name=${name}&room=${room}`}>
                    <button type = "submit">Sign In</button>
                </Link>
            </div>
        </div>        
    )
}

export default Login