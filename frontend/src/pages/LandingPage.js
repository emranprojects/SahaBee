import appPaths from "../appPaths";
import "./LandingPage.css"
import React from "react";

export default function LandingPage() {
    return <>
        <div className="main-wrapper">
            <div className="section bg col-xs-9">
                <img src="/logo192.png"/>
                <h1 className="text-center font-weight-bold text-white stroke-black">SahaBee</h1>
                <h3 className="text-center font-weight-bold font-italic">Let the good times roll!</h3>
                <a href={appPaths.register} className="btn btn-secondary">Get Started!</a>
            </div>
        </div>
    </>
}