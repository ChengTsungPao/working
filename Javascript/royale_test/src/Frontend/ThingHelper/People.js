import React from 'react'
import { KeyboardEvent } from './KeyboardEvent'
import { useContext } from 'react'
import { positionContext, peopleContext } from './factory'
import { keyboardSupport } from './ThingIndex'

function People() {
    const position = useContext(positionContext);
    const people = useContext(peopleContext);

    window.addEventListener('keydown', function(event){
        KeyboardEvent(event, position, people)
    });
    window.addEventListener('keyup', function(event){
        keyboardSupport.press = false;
    });
    
    
    return (
        <div>
            {people.get}
        </div>
    )
}

export default People
