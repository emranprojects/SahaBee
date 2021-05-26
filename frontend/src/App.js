import React, {useState} from 'react';

import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import './App.css';
import {HCenter} from "./HCenter";

function App() {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    function login() {
        alert("TODO: Tried to log in!")
    }

    return (
        <Container>
            <Row className="mb-5"/>
            <HCenter md={4}>
                <Card>
                    <Card.Header>Welcome to SahaBee</Card.Header>
                    <Card.Body>
                        <Form>
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
                            <Button variant="primary" type="submit" onClick={login}>Login</Button>
                        </Form>
                    </Card.Body>
                </Card>
            </HCenter>
        </Container>
    );
}

export default App;
