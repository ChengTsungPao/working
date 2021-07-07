import GetData from './GetData'
import { data } from './DataHelper/Restore'
import { client_data_or_not } from '../Start/Config/Contants'

function UpdateData(getData) {
    if(client_data_or_not){
        return;
    }

    // console.log(`${getData} socket on !!!`)

    let socket = GetData("socket");

    socket.on(getData, (retData) => {
        data["gameData"] = retData;

    });
}

export default UpdateData
