import { SetupID } from './SetupID'
import { SetupRoom } from './SetupRoom';
import { SetupMap } from './SetupMap';
import { SetupName } from './SetupName';

export function Setup(name) {
    SetupName(name);
    return {"ID": SetupID(), "Room": SetupRoom(), "map": SetupMap()};
}

