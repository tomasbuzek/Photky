import React from 'react';
import { BrowserRouter, Redirect, Route, Switch } from 'react-router-dom';

import { AppBar, Divider, Drawer, IconButton, Link, List, ListItem, ListItemIcon, ListItemText, Menu, MenuItem, Toolbar, Typography } from '@material-ui/core';
import AccountCircle from '@material-ui/icons/AccountCircle';
import DeleteIcon from '@material-ui/icons/Delete';
import PhotoLibraryIcon from '@material-ui/icons/PhotoLibrary';
import PhotoAlbumIcon from '@material-ui/icons/PhotoAlbum';

import './App.css';

import Styles from './components/styles';
import useJWT from './components/useJWT';
import SignIn from './components/SignIn';
import SignUp from './components/SignUp';

function PrivateRoute({ children, ...rest }) {
  const token = useJWT().token;
  return (
    <Route {...rest} render={({ location }) =>
      token ? (children) : (
        <Redirect to="/login" />
      )
    } />
  );
}

function ListItemLink(props) {
  return <ListItem button component="a" {...props} />;
}

function App() {
  const classes = Styles();
  const [anchorAccountMenu, setAccountMenu] = React.useState(null);

  const accountMenuIsOpened = Boolean(anchorAccountMenu);

  const handleAccountMenu = (event) => {
    setAccountMenu(event.currentTarget);
  };

  const handleAccountMenuClose = () => {
    setAccountMenu(null);
  };

  const logout = () => {
    handleAccountMenuClose();
    clearToken();
  };

  const { token, setToken, clearToken } = useJWT();

  return (
    <div className={classes.root}>
      <AppBar position="fixed" className={classes.appBar}>
        <Toolbar>
          <Typography variant="h6" className={classes.title}>
            <Link href="/" color="inherit">Photky</Link>
          </Typography>
          {token && (
            <div>
              <IconButton
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                color="inherit"
                onClick={handleAccountMenu}>
                <AccountCircle />
              </IconButton>
              <Menu id="menu-appbar"
                    anchorEl={anchorAccountMenu}
                    anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
                    keepMounted
                    transformOrigin={{ vertical: 'top', horizontal: 'right' }}
                    open={accountMenuIsOpened}
                    onClose={handleAccountMenuClose}>
              <MenuItem onClick={handleAccountMenuClose} component={Link} href="/profile">Profile</MenuItem>
              <Divider />
              <MenuItem onClick={logout}>Logout</MenuItem>
            </Menu>
            </div>
          )}
        </Toolbar>
      </AppBar>
      <Drawer
        className={classes.drawer}
        variant="permanent"
        classes={{
          paper: classes.drawerPaper,
        }}>
        <Toolbar />
        <div className={classes.drawerContainer}>
          <List>
            {[
              ['All Photos', <PhotoLibraryIcon />, '/photos'],
              ['Albums', <PhotoAlbumIcon />, '/albums'],
              ['Trash', <DeleteIcon />, '/trash']
            ].map((data, index) => (
              <ListItemLink button key={data[0]} href={data[2]}>
                  <ListItemIcon>{data[1]}</ListItemIcon>
                  <ListItemText primary={data[0]} />
              </ListItemLink>
            ))}
          </List>
        </div>
      </Drawer>
      <main className={classes.content}>
        <Toolbar />
        <BrowserRouter>
            <Switch>
              <PrivateRoute exact path="/">
                <Redirect to="/photos" />
              </PrivateRoute>
              <Route path="/login">
                <SignIn setToken={setToken}/>
              </Route>
              <Route path="/signup">
                <SignUp setToken={setToken}/>
              </Route>
              <PrivateRoute path="/photos" />
              <PrivateRoute path="/albums" />
              <PrivateRoute path="/trash" />
              <PrivateRoute path="/profile" />
            </Switch>
          </BrowserRouter>
        </main>
    </div>
  )
}

export default App;
