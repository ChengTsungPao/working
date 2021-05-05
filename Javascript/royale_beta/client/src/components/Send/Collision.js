
export function CollisionEvent(name, pos, data, rad){
    for(var i = 0; i < data.length; i++){
        if(name !== data[i][0] && (data[i][2] - pos[0]) ** 2 + (data[i][3] - pos[1]) ** 2 < (2 * rad) ** 2){ 
            return {event: true, name: data[i][0], posx: data[i][2], posy: data[i][3]}
        }
    }
    return {event: false}
}