import React from 'react'

function BlobComp(props) {
    const [ID, posx, posy, rad] = [props.data.name, props.data.pos[0], props.data.pos[1], props.data.rad];
    return (
        <div>
            <svg id = {ID} height={rad * 2} width={rad * 2} style = {{left: (posx - rad) + 'px', top: (posy - rad) + 'px', position:'absolute'}}>
                <circle cx={rad} cy={rad} r={rad} fill="red" />
            </svg> 
        </div>
    )
}

export default BlobComp
