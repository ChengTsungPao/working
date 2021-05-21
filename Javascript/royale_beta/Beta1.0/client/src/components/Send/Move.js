
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


