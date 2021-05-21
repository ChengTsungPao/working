import React from 'react'

function Wall1(props) {
    const [name, posx, posy] = [props.data[0], props.data[2], props.data[3]];
    return (
        <div>
            <svg id = {name} width="50" height="100" style = {{left: posx + 'px', top: posy + 'px', position:'absolute'}}>
                <rect width="50" height="100" />
            </svg>
        </div>
    )
}

export default Wall1
