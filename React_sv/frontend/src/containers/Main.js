import React from 'react';
import { connect } from 'react-redux';

const Main = ({ isAuthenticated, user }) => {
  if (user && Object.keys(user).length > 0) {
    return (
      <div>
        You are {isAuthenticated ? 'Login' : 'Not Login'}, Welcome to {user.username}
      </div>
    );
  } else {
    return <div>No user information available</div>;
  }
};

const mapStateToProps = (state) => ({
  isAuthenticated: state.auth.isAuthenticated,
  user: state.auth.user_information,
});

export default connect(mapStateToProps)(Main);

