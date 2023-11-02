import React from 'react'
import { useState } from 'react';
import {Navigate} from 'react-router-dom'
import { reset_password } from '../actions/auth';
import { connect } from 'react-redux';

const ResetPassword = ({reset_password}) => {
  const [Request, SetRequest] = useState(false);
  const [formData, setFormData] = useState({ email: ''});
  const { email } = formData;

  const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = e => {
    e.preventDefault();  
    reset_password(email)
    SetRequest(true)
  };

  if (Request){
    return(<Navigate to={'/notification/'} />);
  }

  return (
    <div className='container mt-5'>
        <h1>Request Password Reset:</h1>
        <form onSubmit={e => onSubmit(e)}>
            <div className='form-group'>
                <input
                    className='form-control'
                    type='email'
                    placeholder='Email'
                    name='email'
                    value={email}
                    onChange={e => onChange(e)}
                    required
                />
            </div>
            <button className='btn btn-primary' type='submit'>Send Request to your Emal</button>
        </form>
    </div>
);
}

export default connect(null,{reset_password}) (ResetPassword);
