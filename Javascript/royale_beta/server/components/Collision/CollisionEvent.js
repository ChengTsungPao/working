
module.exports = function(){
    this.CollisionEvent = function(name, pos, data, rad){
        for(var i = 0; i < data.length; i++){
            if(name !== data[i][0] && (data[i][2] - pos[0]) ** 2 + (data[i][3] - pos[1]) ** 2 < (2 * rad) ** 2){ 
                return {event: true, name: data[i][0], posx: data[i][2], posy: data[i][3], index: i}
            }
        }
        return {event: false}
    }
    this.MoveCollision = function(posA, posB, speed){
        var vector = [posB[0] - posA[0], posB[1] - posA[1]]
        return [speed * vector[0] / (vector[0] ** 2 + vector[1] ** 2) ** 0.5, speed * vector[1] / (vector[0] ** 2 + vector[1] ** 2) ** 0.5]
    }
}

