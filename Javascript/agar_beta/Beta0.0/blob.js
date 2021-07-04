function Blob(x, y, r) {
    this.pos = createVector(x, y);
    this.r = r;
    this.vel = createVector(0, 0);

    this.update = function() {
        // origin
        // var vel = createVector(mouseX, mouseY);
        // vel.sub(this.pos);
        // vel.setMag(3);
        // this.pos.add(vel);
        
        // change
        // var vel = createVector(mouseX - width / 2, mouseY - height / 2);
        // vel.setMag(3);
        // this.pos.add(vel);

        // final
        var newvel = createVector(mouseX - width / 2, mouseY - height / 2);
        newvel.setMag(3);
        this.vel.lerp(newvel, 0.1);
        this.pos.add(this.vel);
    }

    this.eats = function(other) {
        var d = p5.Vector.dist(this.pos, other.pos);
        if (d < this.r + other.r) {
            // this.r += other.r * 0.2;
            var sum = PI * this.r * this.r + PI * other.r * other.r
            this.r = sqrt(sum / PI);
            return true;
        } else {
            return false;
        }
    }

    this.show = function() {
        fill(255);
        ellipse(this.pos.x, this.pos.y, this.r * 2, this.r * 2)
    }
}