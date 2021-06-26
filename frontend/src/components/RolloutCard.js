import React from "react";
import {Button, Card} from "react-bootstrap";
import {faBell} from "@fortawesome/free-solid-svg-icons";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import utils, {DateFormat} from "../utils";
import apiURLs from "../apiURLs";
import {toast} from "react-toastify";

export default function RolloutCard({onRollcall = (rollout) => undefined}) {
    async function rollcall() {
        const resp = await utils.post(apiURLs.rollouts)
        if (resp.status === 201) {
            const rollout = await resp.json()
            toast.success(<span>Rollout done!<br/>{utils.formatDateTime(rollout.time, DateFormat.TIME)}</span>)
            onRollcall(rollout)
        } else {
            toast.error(`Unexpected status code (${resp.status}): ${await resp.text()}`)
        }
    }

    return <Card>
        <Card.Body>
            <Button className="btn-block btn-light btn-outline-info" onClick={rollcall}>
                <FontAwesomeIcon icon={faBell}/><br/>Rollcall!
            </Button>
        </Card.Body>
    </Card>
}