import React, { Component } from 'react'

class Welcome extends Component {
    render(){
        const {name, hn} = this.props
        return (
            <h1>
                Welcome {name} a.k.a {hn}
            </h1>
        )
    }
}

export default Welcome