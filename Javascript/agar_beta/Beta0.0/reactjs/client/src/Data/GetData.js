import { data, socket } from './DataHelper/Restore'

function GetData(kind) {
    switch (kind) {
        case "_id":
            return data["_id"]
        case "name":
            return data["name"];
        case "room":
            return data["room"];
        case "gameData":
            return data["gameData"];
        case "socket":
            return socket
        default:
            return null;
    }

}

export default GetData;
