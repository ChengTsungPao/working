const gv_ = require('../globalVariable');
const guid = require('../functions/guid');
const SetRoomBroadcast = require('./broadcast');

module.exports = socket_settings = (io) => {
    io.on('connection', (socket) => {
        
        socket.on('SetRoom', (data) => {
            let _id = data['_id']

            let username = data['username'] //要去DB取得
            
            let room = data['room']
            let tick = 64 || data['tick'] 

            if (room == null) {
                room = guid()
            }

            

            gv_.addUser(_id, username, room, tick);
            socket.join(room);

            //for test
            for(let i = 0; i<25 ; i++){
                let tmp_id = guid()
                gv_.addUser(tmp_id, null, room, 60);
                gv_.setUserInfo(tmp_id, null, room, [Math.random() * 1500,  Math.random() * 750], 15, [0,0], "LIVE")
            }

            SetRoomBroadcast(io, room);
            socket.emit('getRoom', { 'room': room , "_id" : _id});
        })

        //設定/更新Blob狀態
        socket.on('setBlob', (data) => {
            // data = 使用者資料
         
            let _id = data['_id']
            let pos = data['pos']
            let name = data['name']
            let room = data['room']
            let vel = data['vel']
            let rad = data['rad']
            let state = data['state']

            if(state==='DEAD'){
                gv_.removeUserFromRoom(_id);
            }
            else{
                gv_.setUserInfo(_id, name, room, pos, rad, vel, state)
            }
            /*
            '_id' : data['_id'],
            update_data = new Blob(){
                'kind' : data['kind'],
                'name' : data['name'],
                'room' : data['room'],
                'vel' : data['vel'],
                'rad' : data['rad'],
                'state' : data['state'],
            };
            */

            // 設定使用者資訊
            
        })

        socket.on('disconnect', () =>{
            socket.emit('disconnected');
        })

        socket.on('leftRoom', (_id) =>{ // either client disconnect or leave room call this 
            gv_.removeUserFromRoom(_id);
        })

        socket.on('getData', (data) =>{
            var retData = {}
            var _id = data['_id']
            var kind = data['kind']
            let ret_Data = ""
            switch(kind){     
                //根據kind做對應的事
                default:
                    break;
            }
            retData['_id'] = _id;
            retData['kind'] = kind
            retData['data'] = ret_Data
            socket.emit('retData', retData)

        })


    });
}
