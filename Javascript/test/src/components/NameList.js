import React from 'react'
import Person from './Person'

function NameList() {
    const names = [{id: "a", greet: "Hi"}, {id: "b", greet: "Hello"}, {id: "c", greet: "Hey"}]
    // const namelist = names.map(name => <h2>我是傻{name.id} {name.greet}</h2>)
    const namelist = names.map((name, index) => <Person person = {name}/>) //蝦米warning我某阿 ch18
    return (
        <div>
            {/* <h2>{names[0]}</h2>
            <h2>{names[1]}</h2>
            <h2>{names[2]}</h2> */}
            {namelist}
        </div>
    )
}

export default NameList
