import React, {useContext, useEffect} from 'react';
import utils from "../utils";
import LoginContext from "./LoginContext";
import apiURLs from "../apiURLs";
import {toast} from "react-toastify";
import {Spinner} from "react-bootstrap";

export default function OAuthLoginBtn({onLoggedIn = () => undefined}) {
    const loginContext = useContext(LoginContext);

    async function onGoogleSignedIn(googleUser) {
        toast.success("Successfully logged in!")
        const id_token = googleUser.getAuthResponse().id_token;
        const resp = await utils.post(apiURLs.googleUserLogin, {'google_user_id_token': id_token},
            null, false)
        const result = await resp.json()
        utils.setLoggedIn(result.username, result.token)
        loginContext.setIsLoggedIn(true)
        onLoggedIn()
    }

    function onGoogleSignInFailed({error}) {
        toast.error(`Failed to log in with Google. ${error}`)
    }

    useEffect(() => {
        window.gapi.load('auth2', () => {
            window.gapi.auth2.init().then((auth) => {
                auth.signOut().then(() => {
                    window.gapi.signin2.render('google-signin-button', {
                        height: 40,
                        longtitle: true,
                        onsuccess: onGoogleSignedIn,
                        onfailure: onGoogleSignInFailed,
                    });
                });
            });
        });

    }, [])

    return <div id="google-signin-button" className="google-signin-button">
        <Spinner animation="border" variant="info" className="ml-auto mr-2"/>
    </div>
}
