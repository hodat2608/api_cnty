import React from 'react'
import { connect } from 'react-redux'

const Content = ({isAuthenticated}) => {
  if (isAuthenticated){
    console.log('boo: ', isAuthenticated)
  };
  return (
    <div>
      You are {isAuthenticated ? 'Login' : 'Not Login'}, Welcome to you
    </div>
  )
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps)(Content);
