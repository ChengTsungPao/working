import { user, map } from './Restore'

export function GetData(kind) {
    switch (kind) {
        case "ID":
            return user.ID;
        case "Room":
            return user.Room;
        case "name":
            return user.name;
        case "map":
            return map
        default:
            return null;
    }

}
