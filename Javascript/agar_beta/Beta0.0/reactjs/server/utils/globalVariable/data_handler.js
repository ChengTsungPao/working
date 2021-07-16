
module.exports = class Handler {
    constructor() {
        this.user_data = {} // {'_id': {'name', 'room', 'kind', 'r', 'vel'}}
        this.room_data = {} // {'room' : {'_id':[_id], 'tick', 'bullet', 'roomState'}}
        this.roomBroadcastData = {} // {'room': null}
    }

    // 函數名稱修正
    addUser(_id, name, room, tick) {
        // user data
        if (!(_id in this.user_data)) {
            this.user_data[_id] = { 
                'name': name,
                'room': room,
                'pos': [0, 0],
                'rad': 0,
                'vel': [0,0],
                'state':'LIVE'
            }
        }
        else {
            console.log(`[加入使用者異常!] ${_id}你已經在裡面了`);    //未來寫成Log.txt
            return;
        }
        // room data : init
        if (!(room in this.room_data)) {
            this.room_data[room] = { '_id': [], 'tick': tick }
        }
        // 加入使用者socket id
        this.room_data[room]['_id'].push(_id)
    }

    setUserInfo(_id, name, room, pos, rad, vel, state) {
        
        if (!(_id in this.user_data)) {
            return
        }
        // 之後優化
        this.user_data[_id]['name'] = name
        this.user_data[_id]['room'] = room
        this.user_data[_id]['pos'] = pos
        this.user_data[_id]['rad'] = rad        
        this.user_data[_id]['vel'] = vel
        this.user_data[_id]['state'] = state      
    }

    setBlob(_id, name, room, pos, vel, rad, state){
        if(!(this.room_data[_id])){
            return;
        }
    }

    setRoomBroadcastData(room, data) {
        if (!(room in this.roomBroadcastData)) {
            this.roomBroadcastData[room] = null
        }
        this.roomBroadcastData[room] = data
    }

    getAllRoom() {
        return this.room_data;
    }

    getRoomBroadcastData(room) {
        let retData = {}

        // let roomData = this.room_data //copy
        if (room in this.room_data) {
            let player_id_list = this.room_data[room]['_id']

            for (let player_id of player_id_list) {
                let tmp_user_data = this.user_data[player_id]
                retData[player_id] = tmp_user_data;
            }
        }
        //console.log(retData);
        return retData;
    }

    getAllBroadCastRoomData() {
        return this.roomBroadcastData;
    }

    getAllUsersName() {
        let names = []
        for (let _id in this.user_data) {
            let username = this.user_data[_id]['name'];
            names.push(username);
        }
        return names
    }

    getAllUserInfoList() {
        let ret = []
        for (let _id in this.user_data) {
            let name = this.user_data[_id]['name']
            let room = this.user_data[_id]['room']
            let kind = this.user_data[_id]['kind']
            let r = this.user_data[_id]['r']
            ret.push({ '_id': _id, 'r': r, 'name': name, 'room': room, 'kind': kind })
        }
        return ret
    }

    getRoomTick(room) {
        if (!(room in this.room_data)) {
            return 64;  //未來改成讀取全域設定檔變數
        }
        let tick = 0
        tick = this.room_data[room]['tick']
        return tick
    }


    removeUserFromRoom(_id){
        //console.log(this.user_data[_id])
        if(!(_id in this.user_data)){
            return;
        }

        let index = this.room_data[(this.user_data[_id]['room'])]['_id'].indexOf(_id)       //find _id index in room.
        //console.log(index)
        if(index>-1){
            let rid = this.user_data[_id]['room']
            this.room_data[rid]['_id'].splice(index,1)          //delete _id in room_data once find out.
            //console.log("--------Len:",this.room_data[rid]['_id'].length)
        }
        delete this.user_data[_id];
    }


    removeUserAllData(_id){
        this.removeUserFromRoom(_id)
        if(_id in this.user_data){
            delete this.user_data[_id];
        }
    }

    roomEmpty(room){
        
        //var roomData =  this.room_data[room]['_id']
        /*
        for(let user in roomData)
            if(user['state']!="DISCONNECTED"){
                return false;
        }
        console.log(roomData['_id'].length)
        */
        return false;
    }
}