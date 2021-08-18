import React, {useState} from "react";
import {Button, Card, Col, Row} from "react-bootstrap";
import {faBell, faPlus} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import utils, {DateFormat} from "../utils";
import apiURLs from "../apiURLs";
import {toast} from "react-toastify";
import {Redirect} from "react-router-dom";
import appPaths from "../appPaths";

export default function RolloutCard({onRollcall = (rollout) => undefined}) {
    const [tokenInvalid, setTokenInvalid] = useState(false)

    if (!utils.isLoggedIn() || tokenInvalid)
        return <Redirect to={appPaths.login}/>

    async function rollcall() {
        const resp = await utils.post(apiURLs.rollouts)
        switch (resp.status) {
            case 201:
                const rollout = await resp.json()
                toast.success(<span>Rollout done!<br/>{utils.formatDateTime(rollout.time, DateFormat.TIME)}</span>)
                onRollcall(rollout)
                break;
            case 401:
                toast.error("Not logged in!")
                setTokenInvalid(true)
                break;
            default:
                toast.error(`Unexpected status code (${resp.status}): ${await resp.text()}`)
                break;
        }
    }

    return <Card>
        <Card.Body>
            <Row>
                <Col md={10}>
                    <Button className="btn-block btn-light btn-outline-info" onClick={rollcall}>
                        <FontAwesomeIcon icon={faBell}/><br/>Rollcall!
                    </Button>
                </Col>
                <Col md={2}>
                    <a href={appPaths.addRollout} className="btn-block btn btn-info">
                        <FontAwesomeIcon icon={faPlus}/><br/>Custom Rollout
                    </a>
                </Col>
            </Row>
        </Card.Body>
    </Card>
}