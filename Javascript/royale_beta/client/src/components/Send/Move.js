
export function GetPosition(name){
    return [parseInt(document.getElementById(name).style.left.split('px')[0]), parseInt(document.getElementById(name).style.top.split('px')[0])]
}

export function Move(key, speed) {

    switch (key) {
        case "ArrowUp":
            return [0, -speed];
        case "ArrowDown":
            return [0, speed];
        case "ArrowLeft":
            return [-speed, 0];
        case "ArrowRight":
            return [speed, 0];
        default:
            return [0, 0];
      }
    
}

export function MoveCollision(posA, posB, speed) {
    var vector = [posB[0] - posA[0], posB[1] - posA[1]]
    return [speed * vector[0] / (vector[0] ** 2 + vector[1] ** 2) ** 0.5, speed * vector[1] / (vector[0] ** 2 + vector[1] ** 2) ** 0.5]

}


