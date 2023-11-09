import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";
import Paper from "@material-ui/core/Paper";
import Box from "@material-ui/core/Box";
import Grid from "@material-ui/core/Grid";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux'
import { login  } from '../actions/auth';
import {Navigate} from 'react-router-dom';
import axios from 'axios';

const MadeWithLove = () => (
  <Typography variant="body2" color="textSecondary" align="center">
    {"Built with love by the "}
    <Link color="inherit" href="https://material-ui.com/">
      Material-UI
    </Link>
    {" team."}
  </Typography>
);

const useStyles = makeStyles(theme => ({
  root: {
    height: "100vh"
  },
  image: {
    backgroundImage: "url(https://source.unsplash.com/random)",
    backgroundRepeat: "no-repeat",
    backgroundSize: "cover",
    backgroundPosition: "center"
  },
  paper: {
    margin: theme.spacing(8, 4),
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main
  },
  form: {
    width: "70%", // Fix IE 11 issue.
    marginTop: theme.spacing(1)
  },
  submit: {
    margin: theme.spacing(3, 0, 2)
  }
}));

const SignInSide = ({login,isAuthenticated}) => {
  const classes = useStyles();

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
    <Grid container component="main" className={classes.root}>
      <CssBaseline />
      <Grid item xs={false} sm={4} md={7} className={classes.image} />
      <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
        <div className={classes.paper}>
          <Avatar className={classes.avatar}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <form onSubmit = {e => onSubmit(e)} className={classes.form} noValidate>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="username"
              label="Email/Username"
              name="username"
              autoComplete="username"
              autoFocus
              onChange = {e => onChange(e)}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="password"
              onChange = {e => onChange(e)}
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="default"
              className={classes.submit}
            >
              Sign In
            </Button>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="secondary"
              onClick={continueWithGoogle}
              className={classes.submit}
            >
              Continue With Google
          </Button>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            onClick={continueWithFacebook} 
                   
          >
           Continue With Facebook
          </Button>
            <Grid container>
              <Grid className={classes.submit} item xs>
                <Link to={'/reset-password/'} variant="body2">
                  Forgot password?
                </Link>
              </Grid>
              <Grid className={classes.submit} item>
                <Link to={"/SignUp/"} variant="body2">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid>
            <Box mt={5}>
              <MadeWithLove />
            </Box>
          </form>
        </div>
      </Grid>
    </Grid>
  );
};

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated
});
export default connect(mapStateToProps,{login}) (SignInSide);
