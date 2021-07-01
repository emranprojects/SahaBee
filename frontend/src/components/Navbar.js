import React from "react";
import appPaths from "../appPaths";
import {Navbar as BootstrapNavbar} from "react-bootstrap";
import utils from "../utils";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faSignOutAlt} from '@fortawesome/free-solid-svg-icons'
import apiURLs from "../apiURLs";
import LoginContext from "./LoginContext";

export default function Navbar() {

    function logout(loginContext){
        utils.logout()
        loginContext.setIsLoggedIn(false)
    }

    return (
        <LoginContext.Consumer>
            {loginContext =>
                <BootstrapNavbar className="nav-bar" bg="dark" expand="lg">
                    <BootstrapNavbar.Brand href="/" className="text-white">SahaBee</BootstrapNavbar.Brand>
                    <a href={apiURLs.BASE_URL} target="_blank" className="btn btn-dark">API</a>
                    {loginContext.isLoggedIn ? <>
                            <a href={appPaths.dashboard} className="btn btn-dark">Dashboard</a>
                            <a href="/" className="btn btn-dark" onClick={() => logout(loginContext)}>
                                <abbr title="Logout"><FontAwesomeIcon icon={faSignOutAlt}/></abbr>
                            </a>
                        </> :
                        <a href={appPaths.login} className="btn btn-dark">Login</a>
                    }
                </BootstrapNavbar>
            }
        </LoginContext.Consumer>
    )
}
