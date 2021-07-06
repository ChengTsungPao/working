import GetData from './GetData'
import { data } from './DataHelper/Restore'

const TEST = true;

// 測試使用
function PushData(newData){
    var exist = false
    for(let i = 0; i < data["gameData"].length; i++){
        if(data["gameData"][i]["name"] === newData["name"]){
            data["gameData"][i]["pos"] = newData["name"]
            data["gameData"][i]["vel"] = newData["vel"]
            exist = false
        }
    }
    if (exist) {
        data["gameData"].push(newData)
    }
    
}


function SendData(setData, data) {
    data["_id"] = GetData("_id")
    data["name"] = GetData("name")
    data["room"] = GetData("room")

    if(TEST){
        PushData(data);
        return;
    }

    let socket = GetData("socket");
    socket.emit(setData, data);

}

export default SendData
