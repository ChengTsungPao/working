class Vector {
    distance(pos1, pos2) {
        let d = 0
        for(var i = 0; i < pos1.length; i++){
            d += (pos1[i] - pos2[i]) ** 2
        }
        return d ** 0.5
    }

    sub(pos1, pos2) {
        let pos = []
        for(var i = 0; i < pos1.length; i++){
            pos.push(pos1[i] - pos2[i])
        }
        return pos
    }

    add(pos1, pos2) {
        let pos = []
        for(var i = 0; i < pos1.length; i++){
            pos.push(pos1[i] + pos2[i])
        }
        return pos
    }

    linear(vel1, vel2, ratio) {
        let vel = []
        for(var i = 0; i < vel1.length; i++){
            vel.push(vel1[i] + ratio * (vel2[i] - vel1[i]))
        }
        return vel
    }

    normalize(vector, newlength = 1) {
        let length = this.distance(vector, [0, 0]);
        let newVector = [vector[0] * newlength / length, vector[1] * newlength / length]
        return newVector
    }
}

export default Vector