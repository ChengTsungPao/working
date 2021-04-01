import React, {useState} from 'react'
import useInput from '../hooks/useInput'

function UserForm() {
    const [firstName, bindFirstname, resetFirstName] = useInput("")
    const [lastName, bindLastname, resetLastName] = useInput("")

    const submitHandler = (e) => {
        e.preventDefault()
        alert(`Hello ${firstName} ${lastName}`)
        resetFirstName()
        resetLastName()
    }

    return (
        <div>
            <form onSubmit = {submitHandler}>
                <div>
                    <label>First name</label>
                    <input type = "text" 
                    // value = {firstName} 
                    // onChange = {(e) => setFirstName(e.target.value)}
                    {...bindFirstname}
                    />
                </div>
                <div>
                    <label>Last name</label>
                    <input type = "text" 
                    // value = {lastName} 
                    // onChange = {(e) => setLastName(e.target.value)}
                    {...bindLastname}
                    />
                </div>
                <button>Submit</button>
            </form>
        </div>
    )
}

export default UserForm
