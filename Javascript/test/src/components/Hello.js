import React from 'react'

const Hello = () => {
    // return (
    //     <div>
    //         <h1>Class Component</h1>
    //     </div>            
    // ); 
    return React.createElement(
        "div", 
        {id: "Hello", className: "Helloclass"}, 
        React.createElement("h1", null, "Hello Component"))
}

export default Hello