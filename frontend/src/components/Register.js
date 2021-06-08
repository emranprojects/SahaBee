import {Button, Card, Container, Form, Row} from "react-bootstrap";
import {HCenter} from "./HCenter";
import {useState} from "react";
import FormCheckInput from "react-bootstrap/FormCheckInput";
import appPaths from "../appPaths";

export default function Register() {
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [password2, setPassword2] = useState("")

    async function register() {
        if (username === "" || email === "" || password === "" || password2 === "") {
            alert("Please fill all the fields.")
            return
        }
        if (password !== password2) {
            alert("The two passwords don't match!")
            return
        }
        alert("TODO: registration not implemented!")
    }

    return (
        <Container>
            <Row className="mb-5"/>
            <HCenter md={4}>
                <Card>
                    <Card.Header>Register at SahaBee</Card.Header>
                    <Card.Body>
                        <Form onSubmit={async e => {
                            e.preventDefault();
                            await register()
                        }}>
                            <Form.Group>
                                <Form.Label>Username</Form.Label>
                                <Form.Control type="username"
                                              placeholder="Enter username"
                                              value={username}
                                              onChange={e => setUsername(e.target.value)}
                                />
                            </Form.Group>
                            <Form.Group>
                                <Form.Label>Email</Form.Label>
                                <Form.Control type="email"
                                              placeholder="Enter email address"
                                              value={email}
                                              onChange={e => setEmail(e.target.value)}
                                />
                            </Form.Group>
                            <Form.Group>
                                <Form.Label>Password</Form.Label>
                                <Form.Control type="password"
                                              placeholder="Enter password"
                                              value={password}
                                              onChange={e => setPassword(e.target.value)}
                                />
                                <Row className="mb-2"/>
                                <Form.Control type="password"
                                              placeholder="Enter password again"
                                              value={password2}
                                              onChange={e => setPassword2(e.target.value)}
                                />
                            </Form.Group>
                            <Button type="submit" variant="success">Register</Button>
                            <Form.Label className="text-muted"><small>
                                By creating an account, you agree to the
                                <a href="https://todo.come!">Terms of Service</a>.
                            </small></Form.Label>
                            <Form.Label>Already have an account? <a href={appPaths.login}>login</a>!</Form.Label>
                        </Form>
                    </Card.Body>
                </Card>
            </HCenter>
        </Container>
    );
}