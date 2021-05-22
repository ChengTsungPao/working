import { GetData } from './GetData'
import { user } from './Restore'

export function LoadData(ID, Room) {
    if(GetData("ID") != null){
        return;
    }

    user.ID = ID;
    user.Room = Room;
    // And Get name、map by Server

}

