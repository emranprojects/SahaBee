import {Redirect} from "react-router-dom"
import utils from "../utils";
import appPaths from "../appPaths";
import {Container, Row} from "react-bootstrap";
import RolloutsList from "./RoulloutsList";

export default function Dashboard() {
    if (!utils.isLoggedIn())
        return <Redirect to={appPaths.login}/>

    return <>
        <Container>
            <Row className="mb-5"/>
            <RolloutsList/>
        </Container>
    </>
}