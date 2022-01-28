import {Col, Container, Row} from "react-bootstrap";
import React, {useState} from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faUserCircle} from "@fortawesome/free-solid-svg-icons";
import utils from "../utils";
import apiURLs from "../apiURLs";
import {Redirect} from "react-router-dom";
import appPaths from "../appPaths";

export default function UsersCheckinStatus() {
    const [users, setUsers] = useState([]);
    const [isCheckedIns, setIsCheckedIns] = useState({});
    const [authorized, setAuthorized] = useState(true)

    utils.useEffectAsync(async () => {
        const resp = await utils.get(apiURLs.allUsers, () => setAuthorized(false))
        if (resp.status === 200) {
            const users = await resp.json()
            console.log(users)
            setUsers(users)
        }
    }, [])

    utils.useEffectAsync(async () => {
        const resp = await utils.get(apiURLs.usersCheckinStatuses, () => setAuthorized(false))
        if (resp.status === 200) {
            const isCheckedIns = await resp.json()
            console.log(isCheckedIns)
            setIsCheckedIns(isCheckedIns)
        }
    }, [])

    if (!utils.isLoggedIn() || !authorized)
        return <Redirect to={appPaths.login}/>

    let userComponents = []
    for (let user of users.sort((u1, u2) => isCheckedIns[u1.id] ? -1 : 1)) {
        userComponents.push(<UserStatus key={user.id} username={user.username}
                                        name={user.first_name + user.last_name}
                                        is_checked_in={isCheckedIns[user.id]}/>)
    }

    return <Container>
        <Row className="mb-5"/>
        <Row className="pl-5">
            {userComponents}
        </Row>
    </Container>
}

function UserStatus({key, username, name, is_checked_in}) {
    return <Col key={key} lg={2} md={3} sm={6} xs={12} className="mb-5">
        <Row className="mb-2">
            <abbr title={is_checked_in ? "Has checked in today!" : "Hasn't checked in yet, or has checked out."}
                  style={{cursor: 'default'}}>
                <FontAwesomeIcon icon={faUserCircle}
                                 style={{fontSize: '70pt', color: is_checked_in ? '#009621' : '#890000'}}
                />
            </abbr>
        </Row>
        <Row>
            <span style={{fontSize: '12pt'}} className="text-center">{name}&nbsp;</span>
        </Row>
        <Row>
            <span style={{fontSize: '10pt'}} className="text-center">@{username}</span>
        </Row>
    </Col>
}
