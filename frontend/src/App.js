import React from 'react';
import { BrowserRouter, Redirect, Route, Switch } from 'react-router-dom';
import { Button } from '@material-ui/core';

import './App.css';

import useJWT from './components/useJWT';
import SignIn from './components/SignIn';
import SignUp from './components/SignUp';

function App() {
  const { token, setToken, clearToken } = useJWT();

  if (!token) {
    return (
      <BrowserRouter>
        <Switch>
          <Route exact path="/">
            <Redirect to="/login" />
          </Route>
          <Route path="/login">
            <SignIn setToken={setToken}/>
          </Route>
          <Route path="/signup">
            <SignUp setToken={setToken}/>
          </Route>
        </Switch>
      </BrowserRouter>
    )
  } else {
    return (
      <Button type="submit" fullWidth variant="contained" color="primary" onClick={clearToken}>
      Logout
      </Button>
    );
  }
}

export default App;
