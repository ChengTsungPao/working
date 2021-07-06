import GetData from '../../Data/GetData'

class BlobSplit {
    // #splitBlob(allBlob) {
    //     var dynamicBlob = [];
    //     var staticBlob = [];
    //     for(let i = 0; i < allBlob.length; i++){
    //         if(allBlob[i]["_id"] === null){
    //             staticBlob.push(allBlob[i])
    //         }else {
    //             dynamicBlob.push(allBlob[i])
    //         }
    //     }
    //     return {"static": staticBlob, "dynamic": dynamicBlob};
    // }
    
    #myBlob(allBlob) {
        var myBlob = undefined;
        var otherBlob = [];
        for(var i = 0; i < allBlob.length; i++){
            if(GetData("_id") === allBlob[i]["_id"]){
                myBlob = allBlob[i];
            } else {
                otherBlob.push(allBlob[i])
            }
        }
        return {"myBlob": myBlob, "otherBlob": otherBlob};
    }

    get(allBlob) {
        return this.#myBlob(allBlob)
    }
}

export default BlobSplit