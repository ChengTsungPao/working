import GetData from './GetData'
import { data } from './DataHelper/Restore'

const TEST = true;

function UpdateData(getData) {
    if(TEST){
        return;
    }

    // console.log(`${getData} socket on !!!`)

    let socket = GetData("socket");

    socket.on(getData, (retData) => {
        data["gameData"] = retData;

    });
}

export default UpdateData
