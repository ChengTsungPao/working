import GetData from './GetData'
import { data } from './DataHelper/Restore'

const TEST = true;

// 測試使用
function PushData(newData){
    var exist = true
    for(let i = 0; i < data["gameData"].length; i++){
        if(data["gameData"][i]["_id"] === newData["_id"]){
            data["gameData"][i]["pos"] = newData["pos"]
            data["gameData"][i]["vel"] = newData["vel"]
            data["gameData"][i]["rad"] = newData["rad"]
            exist = false
        }
    }
    if (exist) {
        data["gameData"].push(newData)
    }
    
}


function SendData(setData, data) {
    if(TEST){
        PushData(data);
        return;
    }

    let socket = GetData("socket");
    socket.emit(setData, data);

}

export default SendData
