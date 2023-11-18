import React from 'react';
import { AppBar, Toolbar, IconButton, Typography, Menu, MenuItem, Avatar,Grid} from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { connect } from 'react-redux';
import MenuIcon from '@mui/icons-material/Menu';
import { useNavigate } from 'react-router-dom';
import { logout } from '../actions/auth';
import { useState } from 'react';

const AccountMenu = ({ isAuthenticated,user,logout }) => {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);
  const navigate = useNavigate();
  const [redirect, setRedirect] = useState(false);
  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleLogout = () => {
    logout();
    setRedirect(true);
    navigate('/login/');
    handleClose(); 
  };
  const handleMyAccount = () => {
    // Implement your my account logic here
    // For example, navigate to the my account page
    // history.push('/myaccount');
    handleClose();
  };
  const handleMyChangepass = () => {
    navigate('/change-password/');
    handleClose();
  }
  if (isAuthenticated && (user && Object.keys(user).length > 0)) {
    return (
      <AppBar position="static">
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <div>
            {/* Menu button */}
            <IconButton size="large" edge="start" color="inherit" aria-label="menu" onClick={handleMenu}>
              {/* <MenuIcon /> */}
            </IconButton>
          </div>
          <div>
            {/* <Avatar alt="User Avatar" src="/path/to/avatar.jpg" />
            <Typography variant="h5" texts sx={{ marginLeft: 1 }}>
              {user.username}
            </Typography>
            <IconButton size="large" color="inherit" aria-label="user" onClick={handleMenu}>              
              <MenuIcon />
            </IconButton> */}
            <Grid container alignItems="center">
            <Grid item>
              {/* Avatar */}
              <Avatar alt="User Avatar" src="/path/to/avatar.jpg" />
            </Grid>
            <Grid item>
              {/* Username */}
              <Typography variant="h5" sx={{ marginLeft: 1 }}>
                {user.username}
              </Typography>
            </Grid>
            <Grid item>
              {/* Menu button */}
              <IconButton size="large" color="inherit" aria-label="user" onClick={handleMenu}>
                <MenuIcon />
              </IconButton>
            </Grid>
          </Grid>
            <Menu
              anchorEl={anchorEl}
              open={open}
              onClose={handleClose}
              onClick={handleClose}
              PaperProps={{
                elevation: 0,
                sx: {
                  // ... (rest of your styles)
                },
              }}
              transformOrigin={{ horizontal: 'right', vertical: 'top' }}
              anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
            >
              <MenuItem>
                <AccountCircleIcon sx={{ mr: 1 }}/>
                My Account
              </MenuItem>
              <MenuItem onClick={handleMyAccount}>My Account</MenuItem>
              <MenuItem onClick={handleLogout}>Logout</MenuItem>  
              <MenuItem onClick={handleMyChangepass}>Change assword</MenuItem>              
            </Menu>
          </div>
        </Toolbar>
      </AppBar>
    );
  }
}

const mapStateToProps = (state) => ({
  isAuthenticated: state.auth.isAuthenticated,
  user: state.auth.user_information,
});

export default connect(mapStateToProps,{ logout })(AccountMenu);
