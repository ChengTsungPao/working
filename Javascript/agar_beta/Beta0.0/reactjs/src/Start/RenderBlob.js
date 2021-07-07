import GetData from '../Data/GetData'

function RenderBlob(blob) {
    setInterval(() => {
        blob.set({opr: "set", data: GetData("gameData")})
    })
}

export default RenderBlob
