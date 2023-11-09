import React from 'react'
import { connect } from 'react-redux'
const Main =  ({isAuthenticated,user}) => {
  if (user) {
    return (
      <div>
        You are {isAuthenticated ? 'Login' : 'Not Login'}, Welcome to you, {
          user.map(userInfo => (
            <span key={userInfo.id}>{userInfo.username}</span>
          ))
        }
      </div>
    );
  } else {
    return <div>No user information available</div>;
  }
      }
      
const mapStateToProps = state => ({
isAuthenticated: state.auth.isAuthenticated,
user: state.auth.user_information
});
  
export default connect(mapStateToProps)(Main);
