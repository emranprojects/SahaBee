import React, {useState} from 'react';

import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import {HCenter} from "./HCenter";
import apiURLs from "../apiURLs"
import {Redirect} from "react-router-dom";
import utils from "../utils";
import appPaths from "../appPaths";
import {toast} from 'react-toastify';

export default function Login() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [loggedIn, setLoggedIn] = useState(utils.isLoggedIn())

    if (loggedIn)
        return <Redirect to={appPaths.dashboard}/>

    async function login() {
        if (username === "" || password === "") {
            toast.error("Enter username/password!")
            return
        }
        const result = await utils.post(apiURLs.login, {
            username: username,
            password: password
        }, false)
        switch (result.status) {
            case 200:
                toast.success("Successfully logged in!")
                utils.setLoggedIn(username, (await result.json()).token)
                setLoggedIn(true)
                break;
            case 400:
                toast.error("Username/Password wrong.")
                break;
            default:
                toast.error(`Unexpected status code (${result.status}): ${await result.text()}`)
        }
    }

    return (
        <Container>
            <Row className="mb-5"/>
            <HCenter md={4}>
                <Card>
                    <Card.Header>Welcome to SahaBee</Card.Header>
                    <Card.Body>
                        <Form onSubmit={async e => {
                            e.preventDefault();
                            await login()
                        }}>
                            <Form.Group>
                                <Form.Label>Username</Form.Label>
                                <Form.Control type="text"
                                              placeholder="Enter username"
                                              value={username}
                                              onChange={e => setUsername(e.target.value)}
                                />
                            </Form.Group>
                            <Form.Group>
                                <Form.Label>Password</Form.Label>
                                <Form.Control type="password"
                                              placeholder="Enter password"
                                              value={password}
                                              onChange={e => setPassword(e.target.value)}
                                />
                            </Form.Group>
                            <Button type="submit" variant="primary">Login</Button>
                            <Row className="mb-3"/>
                            <Form.Label>New to SahaBee? <a href={appPaths.register}>create an account</a>.</Form.Label>
                        </Form>
                    </Card.Body>
                </Card>
            </HCenter>
        </Container>
    );
}
