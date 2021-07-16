const gv_ = require('../globalVariable');

var roomInterval

//設定定期廣播room
SetRoomBroadcast = (io, room) => {
    /*
    if (gv_.roomIsBroadCast(room)) {
        return;
    } else {
        gv_.setRoomBroadcastData(room, null);
    }*/

    tick = gv_.getRoomTick(room);


    roomInterval = setInterval(() => {
        data = gv_.getRoomBroadcastData(room);
        io.to(room).emit('updateGameData', data);
        //console.log(`房間:${room}->當前所有使用者名稱：${room} , TICK = ${tick}`);
        if(gv_.roomEmpty(room)){
            //console.log('interval stop')
            clearInterval(roomInterval)
        }
        
    }, 1000 / tick)
    
}


module.exports = SetRoomBroadcast;


