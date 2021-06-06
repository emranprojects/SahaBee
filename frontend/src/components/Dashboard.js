import {Redirect} from "react-router-dom"
import utils from "../utils";
import appPaths from "../appPaths";

export default function Dashboard() {
    if (!utils.isLoggedIn())
        return <Redirect to={appPaths.login}/>

    return <>
        <h1>You're logged in!</h1>
        <h3>Rollouts will be here!</h3>
    </>
}