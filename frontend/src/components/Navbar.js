import React from "react";
import appPaths from "../appPaths";
import {Nav, Navbar as BootstrapNavbar} from "react-bootstrap";
import utils from "../utils";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faSignOutAlt,} from '@fortawesome/free-solid-svg-icons'
import apiURLs from "../apiURLs";
import LoginContext from "./LoginContext";
import githubIcon from "../static-media/GitHub-Mark-Light-32px.png"

export default function Navbar() {

    function logout(loginContext) {
        utils.logout()
        loginContext.setIsLoggedIn(false)
    }

    return (
        <LoginContext.Consumer>
            {loginContext =>
                <BootstrapNavbar className="navbar ml-auto" bg="dark" expand="lg">
                    <Nav className="container-fluid">
                        <Nav.Item>
                            <BootstrapNavbar.Brand href="/" className="text-white">SahaBee</BootstrapNavbar.Brand>
                        </Nav.Item>
                        <Nav.Item>
                            <a href={apiURLs.apiDocs} target="_blank" className="btn btn-dark">API</a>
                        </Nav.Item>
                        {loginContext.isLoggedIn ? <>
                                <Nav.Item>
                                    <a href={appPaths.dashboard} className="btn btn-dark">Dashboard</a>
                                </Nav.Item>
                                <Nav.Item>
                                    <a href={appPaths.userProfile} className="btn btn-dark">Profile</a>
                                </Nav.Item>
                                <Nav.Item>
                                    <a href={appPaths.usersCheckinStatus} className="btn btn-dark">Coworkers</a>
                                </Nav.Item>
                                <Nav.Item>
                                    <a href="/" className="btn btn-dark" onClick={() => logout(loginContext)}>
                                        <abbr title="Logout"><FontAwesomeIcon icon={faSignOutAlt}/></abbr>
                                    </a>
                                </Nav.Item>
                            </> :
                            <Nav.Item>
                                <a href={appPaths.login} className="btn btn-dark">Login</a>
                            </Nav.Item>
                        }
                        <Nav.Item className="ml-auto">
                            <abbr title="GitHub repo">
                            <a href="https://github.com/emranbm/SahaBee" target="_blank"
                               className="btn btn-dark"><img src={githubIcon}/></a>
                            </abbr>
                        </Nav.Item>
                    </Nav>
                </BootstrapNavbar>
            }
        </LoginContext.Consumer>
    )
}
