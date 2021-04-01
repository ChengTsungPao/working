import React, { Component } from 'react'

const withCounter = (WrappedComponent, incrementNumber) => {
    class WithCounter extends Component{

        constructor(props) {
            super(props)
        
            this.state = {
                 count: 0
            }
        }
    
        incrementCount = () => {
            // this.setState(                        
            //     {count: this.state.count + 1}
            // )
            this.setState(peState => {
                return {count: peState.count + incrementNumber}
            })
        }

        render(){
            console.log(this.props.name)
            return <WrappedComponent count = {this.state.count} incrementCount = {this.incrementCount} {...this.props}/>
        }
    }
    return WithCounter
}

export default withCounter