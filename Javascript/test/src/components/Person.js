import React from 'react'

function Person({person}) {
    return (
        <div>
            <h2>我是傻{person.id} {person.greet}</h2>
        </div>
    )
}

export default Person
