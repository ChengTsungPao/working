import React, { Component } from 'react'

class From extends Component {

    constructor(props) {
        super(props)
    
        this.state = {
             username: '',
             comments: '',
             Topic: "react"
        }
    }

    handleUsernameChange = (event) => {
        this.setState(
            {username: event.target.value}
        )
    }

    handleCommentChange = (event) => {
        this.setState(
            {comments: event.target.value}
        )
    }

    handleTopicChange = (event) => {
        this.setState(
            {Topic: event.target.value}
        )
    }
    
    handleSubmit = (event) => {
        alert(`${this.state.username} ${this.state.comments} ${this.state.Topic}`)
        event.preventDefault() // 不重整頁面
    }

    render() {
        return (
            <form onSubmit = {this.handleSubmit}> //why push the button will run
                <div>
                    <label>Username</label>
                    <input 
                    type = "text" 
                    value = {this.state.username}
                    onChange = {this.handleUsernameChange} 
                    />
                </div>
                <div>
                    <label>Comments</label>
                    <textarea value = {this.state.comments} onChange = {this.handleCommentChange} />
                </div>
                <div>
                    <label>Topic</label>
                    <select value = {this.state.Topic} onChange = {this.handleTopicChange}>   //why should onChane
                        <option value = "react">React</option>
                        <option value = "angular">Angular</option>
                        <option value = "vue">vue</option>
                    </select>
                </div> 
                <button>Submit</button>
            </form>
        )
    }
}

export default From
