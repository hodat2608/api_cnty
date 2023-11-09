import React from "react";
import Button from "@material-ui/core/Button";
import CssBaseline from "@material-ui/core/CssBaseline";
import TextField from "@material-ui/core/TextField";
import { reset_password } from '../actions/auth';
import Grid from "@material-ui/core/Grid";
import Box from "@material-ui/core/Box";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

import { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';


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
    marginTop: theme.spacing(15),
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

const ResetPassword = ({reset_password}) =>  {

  const classes = useStyles();
  const [Request, SetRequest] = useState(false);
  const [formData, setFormData] = useState({ email: ''});
  const { email } = formData;

  const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

  const onSubmit = e => {
    e.preventDefault();  
    reset_password(email)
    SetRequest(true)
  };

  if (Request){
    return(<Navigate to={'/notification/'} />);
  }

  

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Typography component="h1" variant="h5">
          Hãy cùng tìm tài khoản của bạn!
        </Typography>
        <form onSubmit={e => onSubmit(e)} className={classes.form} noValidate>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="email"
                label="Địa chỉ Email"
                name="email"
                autoComplete="email"
                onChange={e => onChange(e)}
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            GỬI YÊU CẦU ĐẶT LẠI MẬT KHẨU 
          </Button>
          <Grid container justify="flex-end">
            <Grid item>
              <Link to={"#"} variant="body2">
                Bạn cần sự trợ giúp ?
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

export default connect(null,{reset_password}) (ResetPassword);
