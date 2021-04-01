import React, { Component } from 'react'
import ComponentF from './ComponentF'
import UserContext from './userContext'

class ComponentE extends Component {
    
    static contextType = UserContext //運行原理想不通

    render() {
        return (
            <div>
                Component E context {this.context}
                <ComponentF />
            </div>
        )
    }
}

// UserContext.contextType = UserContext

export default ComponentE
