import { WIDTH, HEIGHT, RADIUS } from './Contants'
import SendData from '../Data/SendData'
import GetData from '../Data/GetData'
import Vector from './Function/Vector'

class Blob {
    constructor(pos = [HEIGHT / 2, WIDTH / 2], vel = [0, 0], rad = RADIUS) {
        this.pos = pos;
        this.vel = vel;
        this.rad = rad;

        this.newPos = pos;
        this.newVel = vel;
        this.newRad = rad;

        this.cal = new Vector();

        this.#sendData();
    }

    #sendData() {
        var data = {
            "pos": this.newPos,
            "vel": this.newVel,
            "rad": this.newRad
        }
        SendData(data);
    }

    #updataData() {
        let data = GetData("gameData")

        this.pos = data["pos"]
        this.vel = data["vel"]
        this.rad = data["rad"]

        this.newPos = data["pos"];
        this.newVel = data["vel"];
        this.newRad = data["rad"];
    }

    #updatePosVel(mouseX, mouseY) {
        this.newVel = this.cal.sub([mouseX, mouseY], [HEIGHT / 2, WIDTH / 2]);
        this.newVel = this.cal.normalize(this.newVel, 3);
        this.newVel = this.cal.linear(this.vel, this.newVel, 0.1);
        this.newPos = this.cal.add(this.pos, this.newVel);
    }

    #updateCollision(otherBlob) {
        for(var i = 0; i < otherBlob.length; i++) {
            if(this.rad + otherBlob[i].rad < this.cal.distance(this.newPos, otherBlob[i].pos)){
                this.newRad = sqrt((this.rad * this.rad + otherBlob[i].rad * otherBlob[i].rad) / 2);
            }
        }
    }

    update(mouseX, mouseY) {
        this.#updatePosVel(mouseX, mouseY);
        this.#updateCollision();
        this.#sendData();
        this.#updataData();
    }
}

export default Blob