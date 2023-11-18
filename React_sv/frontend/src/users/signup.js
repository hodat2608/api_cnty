import React from 'react'
import { Link } from 'react-router-dom';
import { useState,useEffect } from 'react'
import { connect } from 'react-redux';
import { signup } from '../actions/auth';

const Signup_user = ({signup}) => {
    const [formData, setFormData] = useState({
        email : '',
        username : '',
        password:'',
        password_confirm :''
    });
    const { email, username ,password, password_confirm, } = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });
    
    const onSubmit = e => {
        e.preventDefault();
        if (password === password_confirm) {
            signup(email, username ,password, password_confirm,);
        }
    };
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
                    type='text'
                    placeholder='Username*'
                    name='username'
                    value={username}
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
            <div className='form-group'>
                <input
                    className='form-control'
                    type='password'
                    placeholder='Confirm Password*'
                    name='password_confirm'
                    value={password_confirm}
                    onChange={e => onChange(e)}
                    minLength='6'
                    required
                />
            </div>
            <button className='btn btn-primary' type='submit'>Register</button>
        </form>
        <p className='mt-3'>
            Already have an account? <Link to='/login/'>Sign In</Link>
        </p>
        </div>
    );
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, { signup })(Signup_user);