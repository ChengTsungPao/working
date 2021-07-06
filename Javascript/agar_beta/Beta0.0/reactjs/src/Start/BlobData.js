import { WIDTH, HEIGHT, RADIUS } from './Config/Contants'
import SendData from '../Data/SendData'
import GetData from '../Data/GetData'
import Vector from './Function/Vector'
import BlobSplit from './Function/BlobSplit'
import { mouse } from './Config/Variable'

class BlobData {
    constructor(_id, name, room, pos = [WIDTH / 2, HEIGHT / 2], vel = [0, 0], rad = RADIUS) {
        this._id = _id
        this.name = name
        this.room = room

        this.pos = pos;
        this.vel = vel;
        this.rad = rad;

        this.newPos = pos;
        this.newVel = vel;
        this.newRad = rad;

        this.cal = new Vector();
        this.split = new BlobSplit();

        this.#sendData();
    }

    #sendData() {
        var data = {
             "_id": this._id,
            "name": this.name,
            "room": this.room,
             "pos": this.newPos,
             "vel": this.newVel,
             "rad": this.newRad
        }
        SendData("socketName", data);
    }

    #updataData() {
        let data = this.split.get(GetData("gameData"))["myBlob"];

        this.pos = data["pos"]
        this.vel = data["vel"]
        this.rad = data["rad"]

        this.newPos = data["pos"];
        this.newVel = data["vel"];
        this.newRad = data["rad"];
    }

    #updatePosVel() {
        this.newVel = this.cal.sub([mouse.x, mouse.y], this.pos); // [WIDTH / 2, HEIGHT / 2]
        this.newVel = this.cal.normalize(this.newVel, 3);
        this.newVel = this.cal.linear(this.vel, this.newVel, 0.1);
        this.newPos = this.cal.add(this.pos, this.newVel);
    }

    #updateCollision() {
        var otherBlob = this.split.get(GetData("gameData"))["otherBlob"];
        for(var i = 0; i < otherBlob.length; i++) {
            if(this.rad + otherBlob[i].rad < this.cal.distance(this.newPos, otherBlob[i].pos)){
                this.newRad = ((this.rad * this.rad + otherBlob[i].rad * otherBlob[i].rad) / 2) ** 0.5;
            }
        }
    }

    update() {
        this.#updatePosVel();
        this.#updateCollision();
        this.#sendData();
    }

    show(blobReducer) {
        this.#updataData();
        console.log(this.pos)
        blobReducer.set({opr: "set", data: GetData("gameData")})
    }
}

export default BlobData