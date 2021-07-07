class VectorFcn {

    sub(vector1, vector2) {
        return [vector1[0] - vector2[0], vector1[1] - vector2[1]]
    }

    add(vector1, vector2) {
        return [vector1[0] + vector2[0], vector1[1] + vector2[1]]
    }

    mul(constant, vector) {
        return [constant * vector[0], constant * vector[1]]
    }

    distance(vector1, vector2) {
        return ((vector1[0] - vector2[0]) ** 2 + (vector1[1] - vector2[1]) ** 2) ** 0.5
    }

    linear(vector1, vector2, ratio) {
        return this.add(vector1, this.mul(ratio, this.sub(vector2, vector1)))
    }

    normalize(vector, newlength = 1) {
        let length = this.distance(vector, [0, 0]);
        return this.mul(newlength / length, vector)
    }
}

const Vector = new VectorFcn();

export default Vector