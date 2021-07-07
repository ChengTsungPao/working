import MyBlob from './Object/MyBlob';
import OtherBlob from './Object/OtherBlob';
import Guid from './Function/Guid'
import GetData from '../Data/GetData'
import { WIDTH, HEIGHT } from './Config/Contants'

function CreateBlob() {

    var number = 100;
    // var index = 0

    const myBlob = new MyBlob(GetData("_id"), GetData("name"), GetData("room"))
    
    // 測試模擬地圖
    let otherBlob = []
    for(let i = 0; i < number; i++){
        otherBlob.push(new OtherBlob(Guid(), null, null, [Math.random() * WIDTH, Math.random() * HEIGHT], [0, 0], 5))
        otherBlob[i].show();
    }
    
    setInterval(() => {
        myBlob.update()
        myBlob.show()

        // index = 0
        // while(index < number){
        //     otherBlob[index].update()
        //     otherBlob[index].show()
        //     if(otherBlob[index]["state"] === "dead"){
        //         otherBlob.splice(index, 1)
        //         number -= 1
        //     } else {
        //         index += 1
        //     }
        // }

    }, 1000 / 60)
}

export default CreateBlob
