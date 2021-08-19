import {Button, Card, Container, Form, Row} from "react-bootstrap";
import {HCenter} from "./HCenter";
import {useState} from "react";
import appPaths from "../appPaths";
import {
    GoogleReCaptchaProvider,
    GoogleReCaptcha
} from 'react-google-recaptcha-v3'
import utils from "../utils";
import apiURLs from "../apiURLs";
import {Redirect} from "react-router-dom";
import {toast} from 'react-toastify';

export default function Register() {
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")
    const [password2, setPassword2] = useState("")
    const [recaptcha, setRecaptcha] = useState("")
    const [succeeded, setSucceeded] = useState(false)

    if (succeeded) {
        return <Redirect to={appPaths.login}/>
    }

    async function register() {
        if (username === "" || email === "" || password === "" || password2 === "") {
            toast.error("Please fill all the fields.")
            return
        }
        if (password !== password2) {
            toast.error("The two passwords don't match!")
            return
        }
        if (recaptcha === "" && !utils.isDev()) {
            toast.error("Recaptcha token not set! Inform the admin, please.")
            return
        }

        const resp = await utils.post(apiURLs.register,
            {username, password, email, recaptcha},
            () => undefined,
            false)
        if (resp.status === 201) {
            toast.success("Successfully registered! Try logging in.")
            setSucceeded(true)
        }
    }

    return (
        <GoogleReCaptchaProvider reCaptchaKey="6LcDkycbAAAAAG8DaegS0mox-ITJ1qfDLXiFygVf">
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
                                                  placeholder="Choose a username"
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
                                                  placeholder="Choose password"
                                                  value={password}
                                                  onChange={e => setPassword(e.target.value)}
                                    />
                                    <Row className="mb-2"/>
                                    <Form.Control type="password"
                                                  placeholder="Retype password"
                                                  value={password2}
                                                  onChange={e => setPassword2(e.target.value)}
                                    />
                                </Form.Group>
                                <GoogleReCaptcha action="register" onVerify={setRecaptcha}/>
                                <Button type="submit" variant="success">Register</Button>
                                <Form.Label className="text-muted"><small>
                                    By creating an account, you agree to the
                                    <a href={appPaths.termsOfService}>Terms of Service</a>.
                                </small></Form.Label>
                                <Form.Label>Already have an account? <a href={appPaths.login}>login</a>!</Form.Label>
                            </Form>
                        </Card.Body>
                    </Card>
                </HCenter>
            </Container>
        </GoogleReCaptchaProvider>
    );
}