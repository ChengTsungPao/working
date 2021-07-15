import React from 'react'
import { WIDTH, HEIGHT } from '../../Config/Contants'
import GetData from '../../../Data/GetData';
import { translateRad, translatePos } from './BlobTranslate'
import { scale_or_not } from '../../Config/Contants'

function BlobComp(props) {

    var [_id, data] = props.data;

    var ID = _id;
    var [posx, posy] = ID === GetData("_id") ? [WIDTH / 2, HEIGHT / 2] : translatePos(data["pos"]) // 應該要另外切開，不放在render UI // 在後端處理
    var rad = translateRad(data["rad"])

    if(scale_or_not === false) {
        rad = data["rad"];
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
