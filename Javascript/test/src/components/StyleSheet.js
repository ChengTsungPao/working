import React from 'react'
import MyStyles from './MyStyles.css'

export default function StyleSheet(props) {
    let className
    className = props.primary ? "primary" : ""
    return (
        <div>
            <h1 className = {`${className} font-xl`}>Stylesheets</h1>
        </div>
    )
}
