import GetData from './GetData'
import { data } from './DataHelper/Restore'
import { DEAD } from '../Start/Config/Contants'
import { client_data_or_not } from '../Start/Config/Contants'

// 測試使用
// list version
// function PushData(newData){
//     var exist = true
//     var newDataList = []  // 這邊必須建立新的List直接覆蓋data["gameData"]，不然Reducer的機制會判定狀態沒有改變而不render blob component
    
//     for(let i = 0; i < data["gameData"].length; i++){
//         if(data["gameData"][i]["_id"] === newData["_id"]){
//             exist = false

//             if(newData["state"] === DEAD) {
//                 continue;
//             }

//             newDataList.push(newData)
            
//         } else {
//             newDataList.push(data["gameData"][i])
//         }
//     }
//     if (exist) {
//         newDataList.push(newData)
//     }

//     data["gameData"] = newDataList;
    
// }

// 測試使用
// dict version
function AddData(newData){
    var exist = true
    var newDataDict = {}  // 這邊必須建立新的dict直接覆蓋data["gameData"]，不然Reducer的機制會判定狀態沒有改變而不render blob component
    var id = Object.keys(data["gameData"])

    for(let i = 0; i < id.length; i++){
        if(id[i] === newData["_id"]){
            exist = false

            if(newData["state"] === DEAD) {
                continue;
            }

            newDataDict[id[i]] = newData
            
        } else {
            newDataDict[id[i]] = data["gameData"][id[i]]
        }
    }
    if (exist) {
        newDataDict[newData["_id"]] = newData
    }

    data["gameData"] = newDataDict;
    
}


function SendData(setData, data) {
    if(client_data_or_not){
        // PushData(data);
        AddData(data);
        return;
    }

    let socket = GetData("socket");
    socket.emit(setData, data);

}

export default SendData
