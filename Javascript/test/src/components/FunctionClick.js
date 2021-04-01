import React from 'react'

function FunctionClick() {
    function clickHandler(){
        console.log("Button clicked")
    }

    return (
        <div>
            <button onClick = {clickHandler}>click</button> 
        </div> //無括號 聽不懂 clickHandler()
    )
}

export default FunctionClick

