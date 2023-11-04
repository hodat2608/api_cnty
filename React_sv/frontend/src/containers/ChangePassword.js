import React from 'react'
import { useState } from 'react';
import { connect } from 'react-redux';
import { Navigate } from 'react-router-dom';
import { change_password } from '../actions/auth';

const ChangePassword = ({change_password}) => {

    const [request, SetRequest] = useState(false)
    const [formData,setFormData ] =  useState({
        current_password : '',
        new_password:'',
        re_new_password : '',
    })

    const {current_password,new_password,re_new_password } = formData;
    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();  
        change_password(current_password,new_password,re_new_password)
        SetRequest(true)
      };
    
    if (request){
    return( <Navigate to ='/login/'/>)
    }

  return (
    <div className='container mt-5'>
        <form onSubmit={e => onSubmit(e)}>
            <div className='form-group'>
                <input
                    className='form-control'
                    type='password'
                    placeholder='Current_password*'
                    name='current_password'
                    value={current_password}
                    onChange={e => onChange(e)}
                    minLength='6'
                    required
                />
                <input
                    className='form-control'
                    type='password'
                    placeholder='New Password'
                    name='new_password'
                    value={new_password}
                    onChange={e => onChange(e)}
                    minLength='6'
                    required
                />
                <input
                    className='form-control'
                    type='password'
                    placeholder='Confirm New Password'
                    name='re_new_password'
                    value={re_new_password}
                    onChange={e => onChange(e)}
                    minLength='6'
                    required
                />
            </div>
            <button className='btn btn-primary' type='submit'>Reset Password</button>
        </form>
    </div>
);
}

export default connect(null,{change_password})(ChangePassword);
