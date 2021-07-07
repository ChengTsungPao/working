import React from 'react'
import { WIDTH, HEIGHT, RADIUS } from '../../Config/Contants'
import GetData from '../../../Data/GetData';
import { translateRad, translatePos } from './BlobTranslate'
import { scale_or_not } from '../../Config/Contants'

function BlobComp(props) {

    let ID, posx, posy, rad;
    

    switch (props.data["_id"]) { // 避免抖動，應該要可以拿掉才對(viewShift的方法有誤差)
        case GetData("_id"):
            [ID, posx, posy, rad] = [props.data._id, WIDTH / 2, HEIGHT / 2, RADIUS];
            break;
        default:
            var [posTran, radTran] = [translatePos(props.data.pos), translateRad(props.data.rad)];
            [ID, posx, posy, rad] = [props.data._id, posTran[0], posTran[1], radTran];
            // [ID, posx, posy, rad] = [props.data._id, props.data.pos[0] + view.shift[0], props.data.pos[1] + view.shift[1], props.data.rad];
            break;
    }

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
