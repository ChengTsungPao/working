import React from 'react'

function User1(props) {
    return (
        <div>
            <svg id = { props.data[0] } height="30" width="30" style = {{left: props.data[3] + 'px', top: props.data[4] + 'px', position:'absolute'}}>
                <circle cx="15" cy="15" r="12" stroke="black" fill="red" />
            </svg> 
        </div>
    )
}

export default User1
