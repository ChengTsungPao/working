import HotData from './DataHelper/HotData'
import { data } from './DataHelper/Restore'
import Guid from '../Start/Function/Guid'
import { SETROOMSOCKETNAME, GETROOMSOCKETNAME, SERVERTICK, client_data_or_not } from '../Start/Config/Contants'

export async function SetupRoom(callBack) {
    if(client_data_or_not){
        data["_id"] = Guid();
        data["room"] = "25";
        callBack();
        return;
    }

    let sendData = {
        "_id": Guid(),
        "room": null,
        "tick": SERVERTICK
    }
    let retData = await HotData(SETROOMSOCKETNAME, GETROOMSOCKETNAME, sendData);

    data["_id"] = retData["_id"]
    data["room"] = retData["room"]

    callBack();
}
