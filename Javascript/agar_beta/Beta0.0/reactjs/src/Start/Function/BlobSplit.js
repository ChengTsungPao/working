import GetData from '../../Data/GetData'

function BlobSplit(_id, allBlob) {
    var myBlob = undefined;
    var otherBlob = [];
    for(var i = 0; i < allBlob.length; i++){
        if(_id === allBlob[i]["_id"]){
            myBlob = allBlob[i];
        } else {
            otherBlob.push(allBlob[i])
        }
    }
    return {"myBlob": myBlob, "otherBlob": otherBlob};
}

export default BlobSplit