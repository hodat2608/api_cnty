import React from 'react'
import { useState,useEffect } from 'react'
import { connect } from 'react-redux';
import { login } from '../actions/auth';
import { Link } from 'react-router-dom';
import { Navigate } from 'react-router-dom';

const Login_user = ({login,isAuthenticated}) => {
    const[formData,setFormData] =useState({
        email :'',
        password:'',
    })
    const { email, password } = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });
    
    const onSubmit = e => {
        e.preventDefault();
        login(email, password); 
        console.log(email);
        console.log(password);
        console.log("da submit");
    };

    if (isAuthenticated) {
        console.log("da xac thuc");
        return <Navigate to='/all_note/' />
    }


    return (
    <div className='containerdat mt-5'>
    <h1>Sign Up</h1>
    <p>Create your Account</p>
    <form onSubmit={e => onSubmit(e)}>
        <div className='form-group'>
            <input
                className='form-control'
                type='email'
                placeholder='Email*'
                name='email'
                value={email}
                onChange={e => onChange(e)}
                required
            />
        </div>     
        <div className='form-group'>
            <input
                className='form-control'
                type='password'
                placeholder='Password*'
                name='password'
                value={password}
                onChange={e => onChange(e)}
                minLength='6'
                required
            />
        </div>
        <button className='btn btn-primary' type='submit'>Register</button>
    </form>
    <p className='mt-3'>
        Already have an account? <Link to='/signup/'>Sign In</Link>
    </p>
    </div>
    
    );
}
const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps,{login})(Login_user);
