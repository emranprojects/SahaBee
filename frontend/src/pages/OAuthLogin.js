import React, {useContext, useState} from 'react';

import Form from 'react-bootstrap/Form';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import {HCenter} from "../components/HCenter";
import {Redirect, useLocation} from "react-router-dom";
import utils from "../utils";
import appPaths from "../appPaths";
import LoginContext from "../components/LoginContext";
import {GoogleLogin} from 'react-google-login';

export default function OAuthLogin() {
    const [loggedIn, setLoggedIn] = useState(false)
    const location = useLocation()
    const loginContext = useContext(LoginContext);

    function get_id_token_if_exists() {
        const id_token_arr = location.hash.substr(1)
            .split('&')
            .filter(a => a.split('=')[0] === 'id_token')
            .map(a => a.split('=')[1])
        if (id_token_arr.length === 1)
            return id_token_arr[0]
        else
            return null
    }

    utils.useEffectAsync(async () => {
        const id_token = get_id_token_if_exists()
        if (id_token === null)
            return
        // TODO: Login by user id token
        alert("OAuth login is not implemented currently!")
        setLoggedIn(false)
        loginContext.setIsLoggedIn(false)
    }, get_id_token_if_exists())

    if (loggedIn)
        return <Redirect to={appPaths.dashboard}/>

    return (
        <Container>
            <Row className="mb-5"/>
            <HCenter md={4}>
                <Card>
                    <Card.Header>Welcome to SahaBee</Card.Header>
                    <Card.Body>
                        <GoogleLogin
                            clientId="376753460703-vd3vrq71oblv3nodp18hvf4g1hp4sqo8.apps.googleusercontent.com"
                            buttonText="Login with Google"
                            uxMode="redirect"
                            cookiePolicy={'single_host_origin'}
                        />
                        <Form.Label className="text-muted"><small>
                            By using SahaBee, you agree to the
                            <a href={appPaths.termsOfService}> Terms of Service</a>.
                        </small></Form.Label>
                    </Card.Body>
                </Card>
            </HCenter>
        </Container>
    );
}
