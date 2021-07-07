import { WIDTH, HEIGHT, RADIUS } from '../Config/Contants'
import BlobData from './Blob/BlobData'
import { viewShift } from '../Config/Variable'
import Vector from '../Function/Vector'

class MyBlob extends BlobData {
    constructor(_id, name, room, pos = [WIDTH / 2, HEIGHT / 2], vel = [0, 0], rad = RADIUS) {
        super(_id, name, room, pos, vel, rad)
    }

    setViewShift() {
        const shift = Vector.sub([WIDTH / 2, HEIGHT / 2], this.newPos)
        viewShift.x = shift[0]
        viewShift.y = shift[1]

        // const shift = this.newVel
        // viewShift.x -= shift[0]
        // viewShift.y -= shift[1]
    }

    update() {
        this.updatePosVel();
        this.updateCollision();
        this.setViewShift();
    }

    show() {
        this.sendData();
        this.updataData();
    }

}

export default MyBlob