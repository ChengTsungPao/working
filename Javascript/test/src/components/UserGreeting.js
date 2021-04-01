import React, { Component } from 'react'

export class UserGreeting extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
             isLoggedIn: true
        }
    }
    

    render() {
        return(
            this.state.isLoggedIn ?
            <div>welcome Vishwas</div> :
            <div>welcome Guest</div>
        )

        // let message
        // if (this.state.isLoggedIn) {
        //     message = <div>welcome Vishwas</div>
        // }else{
        //     message = <div>welcome Guest</div>
        // }
        // return message

        // if(this.state.isLoggedIn){
        //     return (
        //         <div>
        //             welcome Vishwas
        //         </div>
        //     )
        // }else{
        //     return (
        //         <div>
        //             welcome Guest
        //         </div>
        //     )
        // }
    }
}

export default UserGreeting
