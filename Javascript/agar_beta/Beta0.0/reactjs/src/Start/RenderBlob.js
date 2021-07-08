import GetData from '../Data/GetData'
import { UITICK } from './Config/Contants'

function RenderBlob(blob) {
    setInterval(() => {
        blob.set({opr: "set", data: GetData("gameData")})
    }, UITICK)
}

export default RenderBlob
