import React, {useEffect, useState} from "react";
import {Card, Table} from "react-bootstrap";
import utils from "../utils";
import apiURLs from "../apiURLs";
import {toast} from "react-toastify";

export default function RolloutsList() {
    const [rollouts, setRollouts] = useState([])

    useEffect(() => {
        let cancel = false;
        (async () => {
            const resp = await utils.get(apiURLs.rollouts)
            if (cancel)
                return
            switch (resp.status) {
                case 200:
                    setRollouts(await resp.json())
                    break;
                default:
                    toast.error(`Unexpected status code (${resp.status}): ${await resp.text()}`)
            }
        })()
        return () => {
            cancel = true
        }
    }, [])

    const rolloutRows = []
    for (let rollout of rollouts)
        rolloutRows.push(<tr>
            <td>{utils.formatDateTime(rollout.time)}</td>
        </tr>)

    return (
        <Card>
            <Card.Header><abbr title="Last 10 reports. Full list will be supported in future versions."><h3>Rollouts</h3></abbr></Card.Header>
            <Table striped={true} bordered={false} hover={true}>
                <tbody>
                {rolloutRows.length > 0 ? rolloutRows : <>
                    <h4 className="text-muted text-center">No rollouts yet.</h4>
                </>}
                </tbody>
            </Table>
        </Card>
    )
}