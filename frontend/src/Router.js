import {BrowserRouter, Route, Switch} from "react-router-dom";
import appPaths from "./appPaths";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import TermsOfService from "./pages/TermsOfService";
import LandingPage from "./pages/LandingPage";
import LoginContext from "./components/LoginContext";
import React, {useState} from "react";
import utils from "./utils";
import UserProfile from "./pages/UserProfile";
import RolloutEditPage from "./pages/RolloutEditPage";
import UsersCheckinStatus from "./pages/UsersCheckinStatus";
import OAuthLogin from "./pages/OAuthLogin";

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
                    <Route path={appPaths.oAuthLogin}>
                        <OAuthLogin/>
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
                    <Route path={appPaths.userProfile}>
                        <UserProfile/>
                    </Route>
                    <Route path={appPaths.addRollout}>
                        <RolloutEditPage/>
                    </Route>
                    <Route path={appPaths.usersCheckinStatus}>
                        <UsersCheckinStatus/>
                    </Route>
                    <Route path="/">
                        <LandingPage/>
                    </Route>
                </Switch>
            </BrowserRouter>
        </LoginContext.Provider>
    )
}