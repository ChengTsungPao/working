import MyBlob from './Object/MyBlob';
import OtherBlob from './Object/OtherBlob';
import Guid from './Function/Guid'
import GetData from '../Data/GetData'
import { WIDTH, HEIGHT, DEAD, DATATICK, OTHERRADIUS, OTHERQUANTITY } from './Config/Contants'

function CreateBlob() {

    const myBlob = new MyBlob(GetData("_id"), GetData("name"), GetData("room"))
    
    // 測試模擬地圖
    let otherBlob = []
    for(let i = 0; i < OTHERQUANTITY; i++){
        otherBlob.push(new OtherBlob(Guid(), null, null, [Math.random() * WIDTH, Math.random() * HEIGHT], [0, 0], OTHERRADIUS))
        otherBlob[i].show();
    }
    
    const myBlobLive = setInterval(() => {
        if(myBlob.state === DEAD){
            clearInterval(myBlobLive);
        }

        myBlob.update()
        myBlob.show()

    }, DATATICK)
}

export default CreateBlob
