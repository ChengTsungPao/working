import React, {useState} from 'react'

function HookCounterTwo() {
    const initialCount = 0
    const [count, setCount] = useState(initialCount)

    const incrementFive = () => {
        for(let i = 0; i < 5; i++){
            setCount((preCount) => {return preCount + 1})
            //setCount(count + 1) wrong !!!
        }
    }

    return (
        <div>
            Count: {count}
            <button onClick = {() => setCount(initialCount)}>Reset</button>
            <button onClick = {() => setCount(count + 1)}>Increment</button>
            <button onClick = {() => setCount(count - 1)}>Decrement</button>
            <button onClick = {incrementFive}>Increment 5</button>
        </div>
    )
}

export default HookCounterTwo
