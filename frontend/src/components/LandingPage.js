import {Redirect} from "react-router-dom"
import utils from "../utils";
import appPaths from "../appPaths";

export default function Rollouts() {
    return <>
        <h1>Landing Page!</h1>
        <a href={appPaths.login} className="btn btn-primary">Login</a>
    </>
}