import React from 'react'

function User1(props) {
    const [name, posx, posy] = [props.data[0], props.data[2], props.data[3]];
    return (
        <div>
            <svg id = { name } height="30" width="30" style = {{left: posx + 'px', top: posy + 'px', position:'absolute'}}>
                <circle cx="15" cy="15" r="12" stroke="black" fill="red" />
            </svg> 
        </div>
    )
}

export default User1
