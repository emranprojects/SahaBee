import React, {useState} from 'react';

import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import {HCenter} from "./HCenter";
import apiURLs from "../apiURLs"

function Login() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    async function login() {
        if (username === "" || password === "") {
            alert("Enter username/password!")
            return
        }
        const result = await fetch(apiURLs.login, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
        switch (result.status) {
            case 200:
                localStorage.setItem('token', (await result.json()).token)
                alert("Login successful!!!")
                break;
            case 400:
                alert("Username/Password wrong.") //TODO nice message
                break;
            default:
                alert(`Unexpected status code (${result.status}): ${await result.text()}`)
        }
    }

    return (
        <Container>
            <Row className="mb-5"/>
            <HCenter md={4}>
                <Card>
                    <Card.Header>Welcome to SahaBee</Card.Header>
                    <Card.Body>
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
                        <Button variant="primary" onClick={login}>Login</Button>
                    </Card.Body>
                </Card>
            </HCenter>
        </Container>
    );
}

export default Login;
