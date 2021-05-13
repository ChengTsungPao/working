import React from 'react'

function User2(props) {
    const [name, posx, posy] = [props.data[0], props.data[2], props.data[3]];
    return (
        <div>
            <svg id = { name } height="24" width="30" style = {{left: posx + 'px', top: posy + 'px', position:'absolute'}}>
                <circle cx="12" cy="12" r="12" fill="green" />
            </svg> 
        </div>
    )
}

export default User2