import { useState } from "react";

const KEY_TOKEN = 'token';

export default function useJWT() {
    const getTokenLocal = () => {
        return JSON.parse(localStorage.getItem(KEY_TOKEN))
    }

    const [token, setTokenToState] = useState(getTokenLocal());

    const storeTokenLocal = userToken => {
        localStorage.setItem(KEY_TOKEN, JSON.stringify(userToken));
        setTokenToState(userToken);
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