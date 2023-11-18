import React from 'react'
import { useState } from 'react';
import { connect } from 'react-redux';
import { Link, Navigate } from 'react-router-dom';
import { change_password } from '../actions/auth';
import { logout } from '../actions/auth';
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


const ChangePassword = ({change_password,isAuthenticated,logout,flag}) => {
    const navigate = useNavigate();
    const [request, SetRequest] = useState(false)
    const [formData,setFormData ] =  useState({
        current_password : '',
        new_password:'',
        re_new_password : '',
    })
    const {current_password,new_password,re_new_password} = formData;
    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });
    const onSubmit = e => {
        e.preventDefault();  
        if(isAuthenticated) {
            if(new_password === re_new_password){
            change_password(current_password,new_password,re_new_password)   
            } else {
                showNotification('Password and confirm password miss match!', 'warning');
            }
        }
      };
    const showNotification = (message, type = 'info') => {
        toast[type](message, {
          position: 'top-center',
          autoClose: 1000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
        });
      };
    const logout_user = () => {
        logout();
        SetRequest(true);
    };
    useEffect(() => {
        if (flag === true) {
          showNotification('Password changed successfully!', 'success');
          setTimeout(() => {
            logout_user();
            navigate('/login');
          }, 2000);
        } else if (flag === false) {
          showNotification('Current Password incorrect!', 'error');
        }
      }, [flag, navigate]);
     
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
const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
    flag : state.auth.flag
  });
export default connect(mapStateToProps,{change_password,logout})(ChangePassword);
