import { WIDTH, HEIGHT, RADIUS, LIVE } from '../Config/Contants'
import BlobData from './Blob/BlobData'

class OtherBlob extends BlobData {
    constructor(_id, name, room, pos = [WIDTH / 2, HEIGHT / 2], vel = [0, 0], rad = RADIUS) {
        super(_id, name, room, pos, vel, rad)
    }

    update() {
        this.updateCollision();
    }

    show() {
        // if(this.state === LIVE){
        //     return;
        // }
        this.sendData();
    }

}

export default OtherBlob