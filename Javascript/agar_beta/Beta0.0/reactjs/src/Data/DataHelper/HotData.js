import { socket } from './Restore'

// 非同步封包寫法
// export async function func() {
//     let ret = await HotData(...)
//         .
// }

function HotData(setData, getData, data) { // setData、getData => socket name

    return new Promise(function (resolve, reject) {

        socket.emit(setData, data);

        socket.once(getData, function (data) {
            resolve(data);
        });

    }).then((result) => {

        return result

    });

}

export default HotData;
