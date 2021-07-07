import GetData from './GetData'
import { data } from './DataHelper/Restore'
import { DEAD } from '../Start/Config/Contants'

const TEST = true;

// 測試使用
function PushData(newData){
    var exist = true
    var newDataList = []  // 這邊必須建立新的List直接覆蓋data["gameData"]，不然Reducer的機制會判定狀態沒有改變而不render blob component
    
    for(let i = 0; i < data["gameData"].length; i++){
        if(data["gameData"][i]["_id"] === newData["_id"]){
            exist = false

            if(newData["state"] === DEAD) {
                continue;
            }

            newDataList.push(newData)
            
        } else {
            newDataList.push(data["gameData"][i])
        }
    }
    if (exist) {
        newDataList.push(newData)
    }

    data["gameData"] = newDataList;
    
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
