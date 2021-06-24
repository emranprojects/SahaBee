import React from "react";
import appPaths from "../appPaths";
import {Navbar as BootstrapNavbar} from "react-bootstrap";

export default function Navbar() {
    return (
        <BootstrapNavbar className="nav-bar" bg="dark" expand="lg">
            <BootstrapNavbar.Brand href="/" className="text-white">SahaBee</BootstrapNavbar.Brand>
            <a href={appPaths.login} className="btn btn-dark">Login</a>
        </BootstrapNavbar>
    )
}
