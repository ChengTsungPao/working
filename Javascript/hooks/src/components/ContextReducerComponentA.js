import React, {useContext} from 'react'
import { CountContext } from '../App'

function ContextReducerComponentA() {
    const countContext = useContext(CountContext)
    return (
        <div>
            ContextReducerComponentA - {countContext.countState}
            <button onClick = {() => countContext.countDispatch('increment')}>Increment</button>
            <button onClick = {() => countContext.countDispatch('decrement')}>Decrement</button>
            <button onClick = {() => countContext.countDispatch('reset')}>Reset</button>
        </div>
    )
}

export default ContextReducerComponentA
