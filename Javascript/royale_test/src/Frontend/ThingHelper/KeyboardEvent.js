import { keyboardSupport } from './ThingIndex'


export function KeyboardEvent(event, position, people) {
    // console.log(event.key)
    if(keyboardSupport.press){
        return;
    }

    switch (event.key) {
        case keyboardSupport.add:
            keyboardSupport.press = true;

            if(position.get.length === 0){
                position.set({operation: "create", pos: [10, 10]})
            }else{
                position.set({operation: "create", pos: [position.get[position.get.length - 1][0] + 60, position.get[position.get.length - 1][1] + 30]})
            }
            people.set({operation: "createPeople", position: position.get})
            break;

        case keyboardSupport.up:
            position.set({operation: "update", pos: [0, -1]})
            break;
            
        case keyboardSupport.down:
            position.set({operation: "update", pos: [0, 1]})
            break;

        case keyboardSupport.left:
            position.set({operation: "update", pos: [-1, 0]})
            break; 

        case keyboardSupport.right:
            position.set({operation: "update", pos: [1, 0]})
            break;   

        default:
            break;
    }

    console.log(position.get)

}

