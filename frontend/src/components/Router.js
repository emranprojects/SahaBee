import {BrowserRouter, Route, Switch} from "react-router-dom";
import appPaths from "../appPaths";
import Navbar from "./Navbar";
import Login from "./Login";
import Register from "./Register";
import Dashboard from "./Dashboard";
import TermsOfService from "./TermsOfService";
import LandingPage from "./LandingPage";
import LoginContext from "./LoginContext";
import React, {useState} from "react";
import utils from "../utils";

export default function Router() {

    const [isLoggedIn, setIsLoggedIn] = useState(utils.isLoggedIn())

    return (
        <LoginContext.Provider value={{isLoggedIn, setIsLoggedIn}}>
            <Navbar/>
            <BrowserRouter>
                <Switch>
                    <Route path={appPaths.login}>
                        <Login/>
                    </Route>
                    <Route path={appPaths.register}>
                        <Register/>
                    </Route>
                    <Route path={appPaths.dashboard}>
                        <Dashboard/>
                    </Route>
                    <Route path={appPaths.termsOfService}>
                        <TermsOfService/>
                    </Route>
                    <Route path="/">
                        <LandingPage/>
                    </Route>
                </Switch>
            </BrowserRouter>
        </LoginContext.Provider>
    )
}