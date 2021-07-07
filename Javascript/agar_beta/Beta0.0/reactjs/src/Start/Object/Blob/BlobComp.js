import React from 'react'
import { viewShift } from '../../Config/Variable'
import { WIDTH, HEIGHT } from '../../Config/Contants'
import GetData from '../../../Data/GetData';

function BlobComp(props) {

    let ID, posx, posy, rad;

    switch (props.data["_id"]) { // 避免抖動，應該要可以拿掉才對(viewShift的方法有誤差)
        case GetData("_id"):
            [ID, posx, posy, rad] = [props.data.name, WIDTH / 2, HEIGHT / 2, props.data.rad];
            break;
        default:
            [ID, posx, posy, rad] = [props.data.name, props.data.pos[0] + viewShift.x, props.data.pos[1] + viewShift.y, props.data.rad];
            break;
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
