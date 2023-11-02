import React from 'react'
import { useState } from 'react';
import { verify } from '../actions/auth';
import {useParams} from 'react-router-dom'
import {Navigate} from 'react-router-dom'
import {connect} from 'react-redux'


const Activate = ({verify}) => {
  const [verified, SetVerified] = useState(false)
  const {uid, token } = useParams();
  const verified_account = e => {
      verify(uid, token);
      SetVerified(true)
  }

  if (verified) {
    return <Navigate to={'/login/'}  />
  }

  return (
    <div className='container'>
        <div 
            className='d-flex flex-column justify-content-center align-items-center'
            style={{ marginTop: '50px' }}
        >
            <h1>Verify your Account:</h1>
            <button
                onClick={verified_account}
                style={{ marginTop: '50px' }}
                type='button'
                className='btn btn-primary'
            >
                Verify
            </button>
        </div>
    </div>
);
}

export default connect(null, { verify })(Activate);
