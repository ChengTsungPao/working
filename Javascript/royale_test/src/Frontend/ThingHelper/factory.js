import { createContext } from 'react'


/* people create and update */

export const peopleContext = createContext()
export const peopleInitial = []
export const peopleReducer = (state, action) => {
    switch (action.operation) {
        case "createPeople":
            return action.position.map((pos, index) => {
                return <button id = {"people_" + index} key = {index} style = {{left: pos[0] + 'px', top: pos[1] + 'px', position:'absolute'}}>哈哈哈</button>
            })
        default:
            return peopleInitial
    }
}

function updatePos(movex, movey, pos) {
    for(var i = 0; i < pos.length; i++){
        pos[i][0] += movex;
        pos[i][1] += movey;
        document.getElementById("people_" + i.toString()).style.left = pos[i][0] + 'px'
        document.getElementById("people_" + i.toString()).style.top = pos[i][1] + 'px'
    }
    return pos;
    
}

export const positionContext = createContext()
export const positionInitial = []
export const positionReducer = (state, action) => {
    switch (action.operation) {
        case "create":
            state.push(action.pos)
            return state
        case "update":
            return updatePos(action.pos[0], action.pos[1], state)
        default:
            return positionInitial
    }
}


/* something create and update */