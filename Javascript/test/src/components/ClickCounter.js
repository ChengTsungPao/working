import React, { Component } from 'react'
import withCounter from './withCounter'

class ClickCounter extends Component {

    // constructor(props) {
    //     super(props)
    
    //     this.state = {
    //          count: 0
    //     }
    // }

    // incrementCount = () => {
    //     this.setState(preState => {
    //         return {count: preState.count + 1}
    //     })
    // }
    
    render() {
        // const {count} = this.state
        const {count, incrementCount} = this.props
        return (
            <div>
                <button onClick = {incrementCount}>{this.props.name} Click {count} times</button>
            </div>
        )
    }
}

export default withCounter(ClickCounter, 5)
