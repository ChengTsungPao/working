import { createContext } from 'react'


export const blobContext = createContext()
export const blobInitial = []
export const blobReducer = (state, action) => {
    switch (action.opr) {
        case "set":
            return action.data
        default:
            return blobInitial
    }
}
