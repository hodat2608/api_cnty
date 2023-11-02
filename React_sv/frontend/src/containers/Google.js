import React, { useEffect }from 'react'
import { GoogleAuthenticate } from '../actions/auth';
import { connect } from 'react-redux';
import { useLocation } from 'react-router-dom';
import queryString from 'query-string'
import { Navigate } from 'react-router-dom';

const Google = ({GoogleAuthenticate}) => {
    let location  = useLocation();

    useEffect(()=> {
        const values = queryString.parse(location.search);
        const state = values.state ? values.state : null ;
        const code = values.code ? values.code : null ;
        
        console.log("state : ", state);
        console.log("code :", code);

        if (state && code ){
            GoogleAuthenticate(state,code)
        }
    },[location]);
    return (
        <div>
            <Navigate to={'/main/'} />
        </div>
    )
}

export default connect(null, {GoogleAuthenticate}) (Google);
