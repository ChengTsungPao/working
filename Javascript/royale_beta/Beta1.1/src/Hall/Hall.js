import React from 'react';
import { Setup } from './Setup/Setup';
import queryString from 'query-string';
import { Link } from 'react-router-dom';

function Hall({ location }) {
    const { name } = queryString.parse(location.search);
    const { ID, Room, map } = Setup(name);

    const StartButton = () => {

    }

    return (
        <div>
            <h1>### Hello {name} ###</h1>
            <h2>Your ID is {ID}</h2>
            <h2>Your Room is {Room}</h2>
            <h2>Your Map is {map.kind}</h2>
            <Link onClick = {StartButton} to = {`/Start?ID=${ID}&Room=${Room}`}>
                    <button type = "submit">Start Gaming</button>
            </Link>
        </div>
    )
}

export default Hall
