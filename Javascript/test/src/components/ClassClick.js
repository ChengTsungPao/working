import React, { Component } from 'react'

class ClassClick extends Component {
    clickHanlder(){
        console.log("click the button")
    }

    render() {
        return (
            <div>
                <button onClick = {this.clickHanlder}>click me</button>
            </div>
        )
    }
}

export default ClassClick
