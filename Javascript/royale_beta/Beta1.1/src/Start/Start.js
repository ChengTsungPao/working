import React, { useEffect } from 'react'
import { user } from '../GetData/Restore'
import { LoadData } from '../GetData/LoadData'
import queryString from 'query-string';

function Start({ location }) {
    
    const { ID, Room } = queryString.parse(location.search);

    useEffect(() => {

        LoadData(ID, Room);

        console.log(user.ID);
        // eslint-disable-next-line
    }, [])


    return (
        <div>
            
        </div>
    )
}

export default Start
