import  { useState } from 'react';
import { TextField, Button, Paper, Typography } from '@mui/material';
import React from 'react'
import { verify } from '../actions/auth';
import {useParams} from 'react-router-dom'
import {Navigate} from 'react-router-dom'
import {connect} from 'react-redux'

const VeryfiedAccount= ({verify}) => {
    const [verified, SetVerified] = useState(false)
    const {uid, token } = useParams();
    const verified_account = e => {
        verify(uid, token);
        SetVerified(true)
    }
    if (verified) {
      return <Navigate to={'/login/'}  />
    }

  return (
    <Paper elevation={3} style={{ padding: 50, maxWidth: 800, margin: 'auto', marginTop: 100 }}>
      <Typography variant="h5" gutterBottom>
        Xác Minh Tài Khoản Của Bạn 
      </Typography>
      <Button variant="contained" color="primary" onClick={verified_account}>
        Xác Minh
      </Button>

      {verified && (
        <Typography variant="body1" style={{ marginTop: 10, color: 'green' }}>
          Xác minh tài khoản thành công!
        </Typography>
      )}
    </Paper>
  );
};

export default connect(null, { verify }) (VeryfiedAccount)
