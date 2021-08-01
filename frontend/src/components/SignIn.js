import React, { useState } from 'react';
import { Button, Container, CssBaseline, TextField, Typography } from '@material-ui/core';
import { Link } from 'react-router-dom';

import Styles from './styles';

async function login(credentials) {
    return fetch('/api/token/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(data => data.text())
    .then(text => {
        const dataJSON = JSON.parse(text);

        if (dataJSON['refresh'] && dataJSON['access']) {
            return dataJSON;
        }

        return null;
    });
}

export default function SignIn({setToken}) {
  const [username, setUsername] = useState();
  const [password, setPassword] = useState();

  const classes = Styles();

  const handleSubmit = async e => {
    e.preventDefault();
    const token = await login({username, password});
    setToken(token);
  }

  return (
      <Container component="main" maxWidth="xs">
          <CssBaseline />
          <div className={classes.paper}>
              <Typography component="h1" variant="h5">
              Sign in
              </Typography>
              <form className={classes.form} noValidate onSubmit={handleSubmit}>
                  <TextField variant="outlined" margin="normal" required fullWidth id="email" label="Email Address" name="email" autoComplete="email" autoFocus onChange={e => setUsername(e.target.value)}/>
                  <TextField variant="outlined" margin="normal" required fullWidth id="password" label="Password" name="password" autoComplete="current-password" type="password" onChange={e => setPassword(e.target.value)} />
                  <Button type="submit" fullWidth variant="contained" color="primary">
                  Sign in
                  </Button>
                  Not a member?
                  <Button component={Link} fullWidth variant="contained" color="secondary" to={'/signup'}>
                  Sign up
                  </Button>
              </form>
          </div>
      </Container>
  );
}