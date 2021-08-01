import { useState } from "react";

const KEY_TOKEN = 'token';

export default function useJWT() {
    const getTokenLocal = () => {
        const tokenJSON = localStorage.getItem(KEY_TOKEN);

        if (typeof tokenJSON === 'undefined') {
            return null;
        }

        return JSON.parse(tokenJSON);
    }

    const [token, setTokenToState] = useState(getTokenLocal());

    const storeTokenLocal = userToken => {
        if (typeof userToken !== 'undefined') {
            localStorage.setItem(KEY_TOKEN, JSON.stringify(userToken));
            setTokenToState(userToken);
        }
    }

    const clearTokenLocal = () => {
        localStorage.removeItem(KEY_TOKEN);
        setTokenToState(null);
    }

    return {
        setToken: storeTokenLocal,
        token,
        clearToken: clearTokenLocal
    }
}