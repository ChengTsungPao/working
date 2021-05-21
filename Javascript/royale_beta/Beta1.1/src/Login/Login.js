import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Login = () => {
    const [name, setName] = useState("");

    return (
        <div>
            <div>
                <h1>Login</h1>
                <div><input placeholder = "Name" type = "text" onChange = {(event) => setName(event.target.value)}/></div>
                <Link onClick = {event => (!name) ? event.preventDefault() : null} to = {`/Hall?name=${name}`}>
                    <button type = "submit">Zoom In Hall</button>
                </Link>
            </div>
        </div>        
    )
}

export default Login