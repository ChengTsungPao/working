
export function GetPosition(name){
    return [parseInt(document.getElementById(name).style.left.split('px')[0]), parseInt(document.getElementById(name).style.top.split('px')[0])]
}

export function Move(name, key, speed) {

    var pos = [];

    switch (key) {
        case "ArrowUp":
            pos = [0, -speed];
            break;
        case "ArrowDown":
            pos = [0, speed];
            break;
        case "ArrowLeft":
            pos = [-speed, 0];
            break;
        case "ArrowRight":
            pos = [speed, 0];
            break;
        default:
            pos = [0, 0];
      }

    const prePos = GetPosition(name);

    document.getElementById(name).style.left = (prePos[0] + pos[0]) + 'px'
    document.getElementById(name).style.top = (prePos[1] + pos[1]) + 'px'
    
}



