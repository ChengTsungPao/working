import { WIDTH, HEIGHT, RADIUS, scale_or_not } from '../Config/Contants'
import BlobData from './Blob/BlobData'
import { view } from '../Config/Variable'
import Vector from '../Function/Vector'

class MyBlob extends BlobData {
    constructor(_id, name, room, pos = [WIDTH / 2, HEIGHT / 2], vel = [0, 0], rad = RADIUS) {
        console.log(WIDTH, HEIGHT)
        super(_id, name, room, pos, vel, rad)
    }

    setViewShift() {
        view.shift = Vector.sub([WIDTH / 2, HEIGHT / 2], this.newPos)
        // view.shift = Vector(view.shift, this.newVel) // 兩個方法皆可以
    }

    setViewZoom() {
        if(scale_or_not === false) {
            return;
        }

        view.zoom = RADIUS / this.newRad
        // view.zoom += (1 - view.zoom) * 0.5
    }

    viewTranslate() {
        this.setViewShift();
        this.setViewZoom();
    }

    update() {
        this.updatePosVel();
        this.updateCollision();
        this.viewTranslate();
    }

    show() {
        this.sendData();
        this.updataData();
    }

}

export default MyBlob