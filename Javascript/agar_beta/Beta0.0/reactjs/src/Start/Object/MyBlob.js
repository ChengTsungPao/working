import { WIDTH, HEIGHT, RADIUS, SCALETARGET, scale_or_not } from '../Config/Contants'
import BlobData from './Blob/BlobData'
import { view, mouse } from '../Config/Variable'
import { show_pos_vel_or_not } from '../Config/Contants'
import Vector from '../Function/Vector'

class MyBlob extends BlobData {
    constructor(_id, name, room, pos = [WIDTH / 2, HEIGHT / 2], vel = [0, 0], rad = RADIUS) {
        super(_id, name, room, pos, vel, rad)
    }

    setViewShift() {
        view.shift = Vector.sub([WIDTH / 2, HEIGHT / 2], this.newPos)
        // view.shift = Vector.sub(view.shift, this.newVel) // 兩個方法皆可以
    }

    setViewZoom() {
        if(scale_or_not === false) {
            return;
        }
        
        // view.zoom ~ RADIUS / this.newRad 內差法
        view.zoom = view.zoom + (RADIUS / this.rad - view.zoom) * SCALETARGET
    }

    viewTranslate() {
        this.setViewShift();
        this.setViewZoom();
    }

    checkStopMyBlob() {
        if (Vector.distance(Vector.sub(mouse.pos, view.shift), this.pos) < this.rad){
            return true;
        } else {
            return false;
        }
    }

    update() {
        this.updatePosVel();
        this.updateCollision();
        this.viewTranslate();
    }

    show() {
        this.sendData();
        this.updataData();
        
        if(show_pos_vel_or_not){
            console.log(`Pos = ${this.pos}`)
            console.log(`Vel = ${this.vel}`)
            console.log(`Rad = ${this.rad}`)
        }
    }

}

export default MyBlob