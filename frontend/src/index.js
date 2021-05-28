import React from 'react';
import ReactDOM from 'react-dom';
import Login from './components/Login';
import reportWebVitals from './reportWebVitals';

import 'bootstrap/dist/css/bootstrap.min.css';
import Rollouts from "./components/Rollouts";
import {BrowserRouter, Route, Switch} from 'react-router-dom';
import appPaths from "./appPaths";

ReactDOM.render(
    <React.StrictMode>
        <BrowserRouter>
            <Switch>
                <Route path={appPaths.login}>
                    <Login/>
                </Route>
                <Route path="/">
                    <Rollouts/>
                </Route>
            </Switch>
        </BrowserRouter>
    </React.StrictMode>,
    document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
