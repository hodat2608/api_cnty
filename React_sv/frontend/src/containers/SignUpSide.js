import React from "react";
import Avatar from "@material-ui/core/Avatar";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import Checkbox from "@material-ui/core/Checkbox";

import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";
import LockOutlinedIcon from "@material-ui/icons/LockOutlined";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

import { useState,useEffect } from 'react';
import { signup } from '../actions/auth';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import axios from 'axios';

function MadeWithLove() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {"Built with love by the "}
      <Link color="inherit" href="https://material-ui.com/">
        Material-UI
      </Link>
      {" team."}
    </Typography>
  );
}

const useStyles = makeStyles(theme => ({
  "@global": {
    body: {
      backgroundColor: theme.palette.common.white
    }
  },
  paper: {
    marginTop: theme.spacing(1),
    display: "flex",
    flexDirection: "column",
    alignItems: "center"
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main
  },
  form: {
    width: "130%", 
    marginTop: theme.spacing(2),
    borderWidth: '2px',  
    borderStyle: 'solid',
    borderColor: '#ccc', 
    borderRadius: '15px', 
    padding: theme.spacing(5),
  },
  submit: {
    margin: theme.spacing(3, 0, 2)
  }
}));

const Signup = ({signup,isAuthenticated}) =>  {

  const classes = useStyles();
  
  const [createdAccount, SetCreatedAccount] = useState(false);
    const [formData, setFormData] = useState({
      email:'',
      username :'',
      password :'',
    })

    const {email,username,password} = formData;

    const onChange = e => setFormData ({...formData,[e.target.name]: e.target.value});

    const onSubmit = e => {
      e.preventDefault();
      signup(email,username,password);
      SetCreatedAccount(true);
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
      return <Navigate to={'/main/'} />
    }

    if (createdAccount){
      return <Navigate to='/login/' />
    }

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign up
        </Typography>
        <form onSubmit={e => onSubmit(e)} className={classes.form} noValidate>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="email"
                label="*Email Address"
                name="email"
                autoComplete="email"
                onChange={e => onChange(e)}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="username"
                label="*Username"
                name="username"
                autoComplete="username"
                onChange={e => onChange(e)}
              />
            </Grid>
            
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                name="password"
                label="*Password"
                type="password"
                id="password"
                autoComplete="password"
                onChange={e => onChange(e)}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControlLabel
                control={<Checkbox value="allowExtraEmails" color="primary" />}
                label="I want to receive inspiration, marketing promotions and updates via email."
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="default"
            className={classes.submit}
          >
            Sign Up
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
          <Grid container justify="flex-end">
            <Grid className={classes.submit} item>
              <Link to={"/login/"} variant="body2">
                Already have an account? Sign in
              </Link>
            </Grid>
          </Grid>
        </form>
      </div>
      <Box mt={5}>
        <MadeWithLove />
      </Box>
    </Container>
  );
}

const mapStateToProps = state => ({
  isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps,{signup}) (Signup) ;