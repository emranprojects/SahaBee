import React from "react";
import {Redirect} from "react-router-dom"
import utils from "../utils";
import appPaths from "../appPaths";
import {Container, Row} from "react-bootstrap";
import RolloutsList from "../components/RoulloutsList";
import RolloutCard from "../components/RolloutCard";
import {useState} from "react";
import TimesheetDownloadCard from "../components/TimesheetDownloadCard";

export default function Dashboard() {
    const [lastAddedRolloutId, setLastAddedRolloutId] = useState()

    if (!utils.isLoggedIn())
        return <Redirect to={appPaths.login}/>

    return <>
        <Container>
            <Row className="mb-5"/>
            <TimesheetDownloadCard lastAddedRolloutId={lastAddedRolloutId}/>
            <RolloutCard onRollcall={(rollout) => setLastAddedRolloutId(rollout.id)}/>
            <RolloutsList lastAddedRolloutId={lastAddedRolloutId}
                          onRolloutDeleted={id => setLastAddedRolloutId(-id)}/>
        </Container>
    </>
}