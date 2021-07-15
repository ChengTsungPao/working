import { blobContext } from '../Core/index';
import { useEffect, useContext, useState } from 'react'
import { mouse } from './Config/Variable'
import BlobComp from './Object/Blob/BlobComp';
import CreateBlob from './CreateBlob';
import RenderBlob from './RenderBlob';

function Start() {
    const blob = useContext(blobContext); // 改名稱
    const [mousePos, setMousePos] = useState([0, 0]);

    const MouseMoveHandler = (event) => {
        setMousePos([event.x, event.y]);
        mouse.pos = [event.x, event.y]
    } 

    /*==================================== Start Process ============================================*/

    useEffect(() => {
        RenderBlob(blob);
        CreateBlob();

        window.addEventListener('mousemove', MouseMoveHandler)
        window.addEventListener('touchmove', MouseMoveHandler)

        // eslint-disable-next-line
    }, [])

    return (
        <div>
            <h>{mousePos[0]} {mousePos[1]}</h>
            {Object.entries(blob.get).map((data, index) => {
                return <BlobComp key={index} data={data} />
            })}
        </div>
    )
}

export default Start
