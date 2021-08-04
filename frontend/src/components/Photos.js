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

    const upload = (event) => {
        let formData = new FormData();

        formData.append("image", event.target.files[0]);

        return axios.post("/api/photos/", formData, {
          headers: {
            'Authorization': 'Bearer ' + accessToken,
            "Content-Type": "multipart/form-data",
          },
        });
      };

    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <input accept="image/*" className={classes.input} id="contained-button-file" multiple type="file" onChange={upload} />
            <Fab color="primary" variant="extended" className={classes.fab} htmlFor="contained-button-file" component="label">
                <AddAPhotoIcon className={classes.extendedIcon} />
                Upload
            </Fab>
        </Container>
    );
}