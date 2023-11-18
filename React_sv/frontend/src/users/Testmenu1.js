import React from 'react'
import { connect } from 'react-redux';
import Avatar from '@mui/material/Avatar';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';

const Testmenu1 = ({ user }) => {
    const [anchorEl, setAnchorEl] = React.useState(null);
  
    const handleMenuOpen = (event) => {
      setAnchorEl(event.currentTarget);
    };
  
    const handleMenuClose = () => {
      setAnchorEl(null);
    };
  
    const handleLogout = () => {
      // Implement your logout logic here
      // For example, dispatch a logout action
      // dispatch(logout());
      handleMenuClose();
    };
  
    const handleMyAccount = () => {
      // Implement your my account logic here
      // For example, navigate to the my account page
      // history.push('/myaccount');
      handleMenuClose();
    };
  
    // Add more menu options and their corresponding handlers as needed
    // if (user && Object.keys(user).length > 0) {
    return (
    
      <div style={{ marginLeft: 'auto' }}>
        <Avatar
          onClick={handleMenuOpen}
          style={{ cursor: 'pointer' }}
          alt="ho thanh dat"
        //   src={user.avatarUrl}
        />
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          onClick={handleMenuClose}
          anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
          transformOrigin={{ vertical: 'top', horizontal: 'right' }}
        >
          <MenuItem onClick={handleMyAccount}>My Account</MenuItem>
          {/* Add more menu options as needed */}
          <MenuItem onClick={handleLogout}>Logout</MenuItem>
        </Menu>
      </div>
    );
  }
// }
  
  const mapStateToProps = (state) => ({
    user: state.auth.user_information,
  });
  
  export default connect(mapStateToProps)(Testmenu1)
