import { blobContext } from '../Core/index';
import { useEffect, useContext, useState } from 'react'
import GetData from '../Data/GetData'
import BlobComp from './BlobComp';
import BlobData from './BlobData';
import { mouse } from './Config/Variable'

function Start() {
    const blob = useContext(blobContext);
    const [mousePos, setMousePos] = useState([0, 0]);

    const MouseMoveHandler = (event) => {
        setMousePos([event.x, event.y]);
        mouse.x = event.x
        mouse.y = event.y
    } 

    /*==================================== Start Process ============================================*/

    useEffect(() => {
        const first = new BlobData(GetData("_id"), GetData("name"), GetData("room"))
        setInterval(() => {
            first.update()
            first.show(blob);
        }, 1000 / 60)

        window.addEventListener('mousemove', MouseMoveHandler)
        window.addEventListener('touchmove', MouseMoveHandler)
    }, [])

    useEffect(() => {
        console.log("123")
    }, [blob.get])


    return (
        <div>
            <h>{mousePos[0]} {mousePos[1]}</h>
            {blob.get.map((data, index) => {
                return <BlobComp key={index} data={data} />
            })}
        </div>
    )
}

export default Start
