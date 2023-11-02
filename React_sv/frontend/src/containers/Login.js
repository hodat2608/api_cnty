import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux'
import { login  } from '../actions/auth';
import {Navigate} from 'react-router-dom';
import axios from 'axios';

const Login = ({login,isAuthenticated}) => {
    const [formData, setFormData] = useState({
      email:'',
      password : '',
    });

    const {username, password} = formData;

    const onChange = e => setFormData ({...formData,[e.target.name]: e.target.value});

    const onSubmit = e => {
      e.preventDefault();  
      login(username,password);
    };

    const continueWithGoogle = async () => {
      try {
          const res = await axios.get(`${process.env.REACT_APP_API_URL}/auth/o/google-oauth2/?redirect_uri=${process.env.REACT_APP_API_URL}/google`)
          window.location.replace(res.data.authorization_url);
      } catch (err) {

      }
    };
    const continueWithFacebook = async () => {
      try {
          const res = await axios.get(`${process.env.REACT_APP_API_URL}/auth/o/facebook/?redirect_uri=${process.env.REACT_APP_API_URL}/facebook`)
          window.location.replace(res.data.authorization_url);
      } catch (err) {

      }
    };

    if (isAuthenticated){
      
      return <Navigate to="/main/" />
    }

    return (
        <div className='containerdat mt-5'> 
          <h1>Sign in</h1>
          <p>Sign in into your account </p>
          <form onSubmit = {e => onSubmit(e)}>
            <div className='form-group'> 
              <input 
                  className='form-control'
                  type='text'
                  placeholder ='Username*'
                  name='username'
                  value = {username}
                  onChange = {e => onChange(e)}
                  required
              />            
            </div>
            <div className='form-group'> 
              <input 
                  className='form-control'
                  type='password'
                  placeholder ='Password '
                  name='password'
                  value = {password}
                  onChange = {e => onChange(e)}
                  minLength= '6'
                  required
              />            
            </div>
            <button className='btn btn-primary' type='submit'>Login</button>
          </form>
          <p className='mt-3'>
            Haven't account yet ? <Link to = '/signup/'>Sign up</Link>
          </p>
          <p className='mt-3'>
            Forgot your password ? <Link to = '/reset-password/'>Forgot password ? </Link>
          </p>
          <button className='btn btn-danger mt-3' onClick={continueWithGoogle}>
              Continue With Google
          </button>
          <br/>
          <button className='btn btn-primary mt-3' onClick={continueWithFacebook}>
              Continue With Facebook
          </button>
        </div>
    );
};
const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});
export default connect(mapStateToProps,{login}) (Login);
