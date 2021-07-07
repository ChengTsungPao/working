import { LIVE, DEAD } from '../../Config/Contants'
import SendData from '../../../Data/SendData'
import GetData from '../../../Data/GetData'
import Vector from '../../Function/Vector'
import BlobSplit from '../../Function/BlobSplit'
import { mouse, view } from '../../Config/Variable'

class BlobData {
    constructor(_id, name, room, pos, vel, rad, state = LIVE) {
        this._id = _id
        this.name = name
        this.room = room
        this.state = state;

        this.pos = pos;
        this.vel = vel;
        this.rad = rad;

        this.newPos = pos;
        this.newVel = vel;
        this.newRad = rad;

        // this.sendData();
    }

    sendData() {
        var data = {
              "_id": this._id,
             "name": this.name,
             "room": this.room,
              "pos": this.newPos,
              "vel": this.newVel,
              "rad": this.newRad,
            "state": this.state
        }
        SendData("socketName", data);
    }

    #removeData(_id) { // 若要刪除需要_id room state
        var data = {
              "_id": _id,
             "name": null,
             "room": this.room,
              "pos": null,
              "vel": null,
              "rad": null,
            "state": DEAD
        }
        SendData("socketName", data);
    }

    updataData() {
        let data = BlobSplit(this._id, GetData("gameData"))["myBlob"];

        this.pos = data["pos"]
        this.vel = data["vel"]
        this.rad = data["rad"]

        this.newPos = data["pos"];
        this.newVel = data["vel"];
        this.newRad = data["rad"];
    }

    updatePosVel() {
        this.newVel = Vector.sub([mouse.x - view.shift[0], mouse.y - view.shift[1]], this.pos); // 滑鼠位置也需要更新
        this.newVel = Vector.normalize(this.newVel, 3);
        this.newVel = Vector.linear(this.vel, this.newVel, 0.1);
        this.newPos = Vector.add(this.pos, this.newVel);
    }

    updateCollision() {
        var otherBlob = BlobSplit(this._id, GetData("gameData"))["otherBlob"];
        for(var i = 0; i < otherBlob.length; i++) {
            if(this.rad + otherBlob[i].rad > Vector.distance(this.newPos, otherBlob[i].pos)){
                if(this.rad > otherBlob[i].rad){
                    this.newRad = (this.rad * this.rad + otherBlob[i].rad * otherBlob[i].rad) ** 0.5;
                    this.#removeData(otherBlob[i]._id)
                } else {
                    this.state = DEAD;
                }
                
            }
        }
    }
}

export default BlobData