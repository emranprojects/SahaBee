import React, {useEffect, useState} from "react";
import {Button, Card, Table} from "react-bootstrap";
import utils from "../utils";
import apiURLs from "../apiURLs";
import {toast} from "react-toastify";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTrash} from "@fortawesome/free-solid-svg-icons";
import {Redirect} from "react-router-dom";
import appPaths from "../appPaths";

export default function RolloutsList({lastAddedRolloutId = null, onRolloutDeleted = id => undefined}) {
    const [rollouts, setRollouts] = useState([])
    const [tokenInvalid, setTokenInvalid] = useState(false)

    useEffect(() => {
        let cancel = false;
        (async () => {
            const resp = await utils.get(apiURLs.rollouts,() => setTokenInvalid(true))
            if (cancel)
                return
            if (resp.status === 200)
                setRollouts(await resp.json())
        })()
        return () => {
            cancel = true
        }
    }, [lastAddedRolloutId])

    if (!utils.isLoggedIn() || tokenInvalid)
        return <Redirect to={appPaths.login}/>

    const rolloutRows = []
    for (let rollout of rollouts)
        rolloutRows.push(<RolloutRow key={rollout.id}
                                     rollout={rollout}
                                     onRolloutDeleted={id => {
                                         setRollouts(rollouts.filter(r => r.id !== id))
                                         onRolloutDeleted(id)
                                     }}/>)

    return (
        <Card>
            <Card.Header><h3>Rollouts</h3></Card.Header>
            {rolloutRows.length > 0
                ? <Table striped={true} bordered={false} hover={true}>
                    <tbody>{rolloutRows}</tbody>

                </Table>
                : <h4 className="text-muted text-center">No rollouts yet.</h4>}
        </Card>
    )
}

function RolloutRow({rollout, onRolloutDeleted}) {
    async function deleteRollout() {
        if (window.confirm(`Delete rollout of "${utils.formatDateTime(rollout.time)}"?`)) {
            const resp = await utils.delete(apiURLs.rollout(rollout.id))
            if (resp.status === 204) {
                toast.success("Rollout deleted.")
                onRolloutDeleted(rollout.id)
            }
        }
    }

    return (
        <tr>
            <td>{utils.formatDateTime(rollout.time)}</td>
            <td className="text-right"><abbr title="Delete rollout">
                <Button variant="danger" onClick={deleteRollout}><FontAwesomeIcon icon={faTrash}/></Button>
            </abbr></td>
        </tr>
    )
}
