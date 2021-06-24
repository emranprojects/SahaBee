import React from 'react';
import ReactDOM from 'react-dom';
import Login from './components/Login';
import reportWebVitals from './reportWebVitals';
import Dashboard from "./components/Dashboard";
import LandingPage from "./components/LandingPage";
import {BrowserRouter, Route, Switch} from 'react-router-dom';
import appPaths from "./appPaths";
import Register from './components/Register';
import {ToastContainer} from 'react-toastify';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-toastify/dist/ReactToastify.css';
import TermsOfService from "./components/TermsOfService";
import Navbar from "./components/Navbar";

ReactDOM.render(
    <React.StrictMode>
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
        <ToastContainer/>
    </React.StrictMode>,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
