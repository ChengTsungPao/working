import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Login = () => {
    const [name, setName] = useState("");
    const [passward, setPassward] = useState("");

    return (
        <div>
            <div>
                <h1>Start</h1>
                <div><input placeholder="name" type="text" onChange={(event) => setName(event.target.value)} /></div>
                <div><input placeholder="passward" type="text" onChange={(event) => setPassward(event.target.value)} /></div>
                <Link onClick={event => true} to={`/Start?name=${name}&passward=${passward}`}>
                    <button type="submit">Zoom In Hall</button>
                </Link>
            </div>
        </div>
    )
}

export default Login