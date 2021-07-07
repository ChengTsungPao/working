import MyBlob from './Object/MyBlob';
import OtherBlob from './Object/OtherBlob';
import Guid from './Function/Guid'
import GetData from '../Data/GetData'
import { WIDTH, HEIGHT, DEAD } from './Config/Contants'

function CreateBlob() {

    var number = 100;
    // var index = 0

    const myBlob = new MyBlob(GetData("_id"), GetData("name"), GetData("room"))
    
    // 測試模擬地圖
    let otherBlob = []
    for(let i = 0; i < number; i++){
        otherBlob.push(new OtherBlob(Guid(), null, null, [Math.random() * WIDTH, Math.random() * HEIGHT], [0, 0], 15))
        otherBlob[i].show();
    }
    
    const myBlobLive = setInterval(() => {
        if(myBlob.state === DEAD){
            clearInterval(myBlobLive);
        }

        myBlob.update()
        myBlob.show()

    }, 1000 / 60)
}

export default CreateBlob
