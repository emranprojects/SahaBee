import {Redirect} from "react-router-dom"
import utils from "../utils";
import appPaths from "../appPaths";
import "./LandingPage.css"
import {HCenter} from "./HCenter";
import Row from "react-bootstrap/Row";
import React from "react";
import {Button, Navbar} from "react-bootstrap";

export default function Rollouts() {
    return <>
        <div className="main-wrapper">
            <Navbar className="nav-bar" bg="dark" expand="lg">
                <Navbar.Brand className="text-white">SahaBee</Navbar.Brand>
                <a href={appPaths.login} className="btn btn-dark">Login</a>
            </Navbar>
            <div className="section bg col-xs-9">
                <img src="/logo192.png"/>
                <h1 className="text-center font-weight-bold text-white stroke-black">SahaBee</h1>
                <h3 className="text-center font-weight-bold font-italic">Let the good times roll!</h3>
                <a href={appPaths.register} className="btn btn-secondary">Get Started!</a>
            </div>
        </div>
    </>
}