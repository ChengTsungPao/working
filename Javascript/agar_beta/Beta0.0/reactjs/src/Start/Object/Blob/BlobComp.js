import React from 'react'
import { WIDTH, HEIGHT, RADIUS } from '../../Config/Contants'
import GetData from '../../../Data/GetData';
import { translateRad, translatePos } from './BlobTranslate'
import { scale_or_not } from '../../Config/Contants'

function BlobComp(props) {

    var ID = props.data._id;
    var [posx, posy] = ID === GetData("_id") ? [WIDTH / 2, HEIGHT / 2] : translatePos(props.data.pos)
    var rad = translateRad(props.data.rad)

    if(scale_or_not === false) {
        rad = props.data.rad;
    }

    return (
        <div>
            <svg id = {ID} height={rad * 2} width={rad * 2} style = {{left: (posx - rad) + 'px', top: (posy - rad) + 'px', position:'absolute'}}>
                <circle cx={rad} cy={rad} r={rad} fill="red" />
            </svg> 
        </div>
    )
}

export default BlobComp
