import React from 'react'
import { useState,useEffect } from 'react'
const login = () => {


  return (
    <div className='container mt-5'>
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
                placeholder='First Name*'
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
    {/* <button className='btn btn-danger mt-3' onClick={continueWithGoogle}>
        Continue With Google
    </button>
    <br />
    <button className='btn btn-primary mt-3' onClick={continueWithFacebook}>
        Continue With Facebook
    </button> */}
    <p className='mt-3'>
        Already have an account? <Link to='/login'>Sign In</Link>
    </p>
    </div>
    );
}

export default login
