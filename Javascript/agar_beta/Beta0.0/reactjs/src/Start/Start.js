import { blobContext } from '../Core/index';
import { useEffect, useContext, useState } from 'react'
import GetData from '../Data/GetData'
import BlobComp from './BlobComp';
import BlobData from './BlobData';

function Start() {
    const blob = useContext(blobContext);
    const [mousePos, setMousePos] = useState([0, 0]);

    /*==================================== Start Process ============================================*/

    useEffect(() => {
        const first = new BlobData(GetData("_id"), GetData("name"), GetData("room"))
        setInterval(() => {
            first.update(mousePos[0], mousePos[1])
            first.show(blob);
        })

    }, [])

    /*===================================== Mouse Event =============================================*/

    const MouseMoveHandler = (event) => {
        setMousePos([event.x, event.y]);
    }

    useEffect(() => {
        window.addEventListener('mousemove', MouseMoveHandler)
        // window.addEventListener('touchmove', MouseMoveHandler)

        return () => {
            window.removeEventListener('mousemove', MouseMoveHandler)
            // window.removeEventListener('touchmove', MouseMoveHandler)
        }
    }, [setMousePos])    

    return (
        <div>
            {blob.get.map((data, index) => {
                return <BlobComp key={index} data={data} />
            })}
        </div>
    )
}

export default Start
