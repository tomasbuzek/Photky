import React, { useState } from 'react';
import { Button, Container, CssBaseline, TextField, Typography, Grid } from '@material-ui/core';

import Styles from './styles';

async function signup(data) {
    return fetch('/api/signup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(data => data.json())
    .then(json => json.token)
}

export default function SignUp({setToken}) {
  const [first_name, setFirstname] = useState();
  const [last_name, setLastname] = useState();
  const [username, setUsername] = useState();
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();

  const classes = Styles();

  const handleSubmit = async e => {
    e.preventDefault();
    const token = await signup({first_name, last_name, username, email, password});
    setToken(token);
  }

  return (
      <Container component="main" maxWidth="xs">
          <CssBaseline />
          <div className={classes.paper}>
              <Typography component="h1" variant="h5">
              Sign up
              </Typography>
              <form className={classes.form} noValidate onSubmit={handleSubmit}>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6}>
                      <TextField autoComplete="fname" name="first_name" variant="outlined" fullWidth id="first_name" label="First Name" autoFocus onChange={e => setFirstname(e.target.value)}/>
                    </Grid>
                    <Grid item xs={12} sm={6}>
                      <TextField variant="outlined" fullWidth id="last_name" label="Last Name" name="last_name" autoComplete="lname" onChange={e => setLastname(e.target.value)}/>
                    </Grid>
                  </Grid>
                  <TextField variant="outlined" margin="normal" required fullWidth id="username" label="Username" name="username" autoComplete="username" onChange={e => setUsername(e.target.value)}/>
                  <TextField variant="outlined" margin="normal" required fullWidth id="email" label="Email Address" name="email" autoComplete="email" onChange={e => setEmail(e.target.value)}/>
                  <TextField variant="outlined" margin="normal" required fullWidth id="password" label="Password" name="password" autoComplete="current-password" type="password" onChange={e => setPassword(e.target.value)}/>
                  <TextField variant="outlined" margin="normal" required fullWidth id="repeatPassword" label="Repeat password" name="repeatPassword" autoComplete="current-password" type="password" />
                  <Button type="submit" fullWidth variant="contained" color="primary">
                  Sign up
                  </Button>
              </form>
          </div>
      </Container>
  );
}