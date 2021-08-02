import React, { useState } from 'react';
import { Container, CssBaseline, Fab } from '@material-ui/core';
import AddAPhotoIcon from '@material-ui/icons/AddAPhoto';

import axios from 'axios';

import Styles from './styles';

export default function Photos({token}) {
    const accessToken = token ? token['access'] : null;

    const [photos, setPhotos] = useState([]);
    const [error, setError] = useState(null);

    const classes = Styles();

    React.useEffect(() => {
        axios.get('/api/photos/', {
            headers: {
                'Authorization': 'Bearer ' + accessToken,
            }
        })
        .then(
            response => {
                setPhotos(response.data);
        })
        .catch(
            error => {
                setError(error);
        });
    }, [accessToken]);

    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <Fab color="primary" variant="extended" className={classes.fab}>
                <AddAPhotoIcon className={classes.extendedIcon} />
                Upload
            </Fab>
        </Container>
    );
}