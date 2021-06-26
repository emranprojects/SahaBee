import React from "react";
import {Redirect} from "react-router-dom"
import utils from "../utils";
import appPaths from "../appPaths";
import {Container, Row} from "react-bootstrap";
import RolloutsList from "./RoulloutsList";
import RolloutCard from "./RolloutCard";
import {useState} from "react";

export default function Dashboard() {
    const [lastAddedRolloutId, setLastAddedRolloutId] = useState()

    if (!utils.isLoggedIn())
        return <Redirect to={appPaths.login}/>

    return <>
        <Container>
            <Row className="mb-5"/>
            <RolloutCard onRollcall={(rollout) => setLastAddedRolloutId(rollout.id)}/>
            <RolloutsList lastAddedRolloutId={lastAddedRolloutId}/>
        </Container>
    </>
}