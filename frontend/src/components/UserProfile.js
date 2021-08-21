import React, {useState} from "react";
import utils from "../utils";
import {Redirect} from "react-router-dom";
import appPaths from "../appPaths";
import {Col, Container, FormControl, InputGroup} from "react-bootstrap";
import apiURLs from "../apiURLs";
import {toast} from "react-toastify";
import EditCard from "./EditCard";

export default function UserProfile() {
    const [userId, setUserId] = useState()
    const [userDetailId, setUserDetailId] = useState()
    const [username, setUsername] = useState("")
    const [email, setEmail] = useState("")
    const [firstname, setFirstname] = useState("")
    const [lastname, setLastname] = useState("")
    const [personnelCode, setPersonnelCode] = useState("")
    const [unit, setUnit] = useState("")
    const [managerName, setManagerName] = useState("")
    const [managerEmail, setManagerEmail] = useState("")
    const [loading, setLoading] = useState(true)
    const [authorized, setAuthorized] = useState(true)


    if (!utils.isLoggedIn() || !authorized)
        return <Redirect to={appPaths.login}/>

    utils.useEffectAsync(fetchUser, [])

    async function fetchUser() {
        const resp = await utils.get(apiURLs.selfUser, () => setAuthorized(false))
        if (resp.status === 200) {
            const user = await resp.json()
            inflateStates(user)
        }
        setLoading(false)
    }

    function inflateStates(user) {
        setUserId(user.id)
        setUsername(user.username)
        setEmail(user.email)
        setFirstname(user.first_name)
        setLastname(user.last_name)
        setUserDetailId(user.detail.id)
        setPersonnelCode(user.detail.personnel_code)
        setUnit(user.detail.unit)
        setManagerName(user.detail.manager_name)
        setManagerEmail(user.detail.manager_email)
    }

    function getUserFromStates() {
        return {
            id: userId,
            username,
            email,
            first_name: firstname,
            last_name: lastname,
            detail: {
                id: userDetailId,
                personnel_code: personnelCode,
                unit,
                manager_name: managerName,
                manager_email: managerEmail
            }
        }
    }

    async function save() {
        if (loading) {
            toast.error("User not loaded yet!")
            return
        }
        const user = getUserFromStates()
        const resp = await utils.put(apiURLs.selfUser, user)
        if (resp.status === 200)
            toast.success("Info updated successfully!")
    }

    return (
        <>
            <EditCard title="Profile Information" onSave={save} loading={loading}>
                <EditCard.Input title="@"
                                value={username}
                                setValueFunc={setUsername}/>
                <EditCard.Input title="Email"
                                value={email}
                                setValueFunc={setEmail}/>
                <EditCard.Input title="Firstname"
                                value={firstname}
                                setValueFunc={setFirstname}/>
                <EditCard.Input title="Lastname"
                                value={lastname}
                                setValueFunc={setLastname}/>
                <EditCard.Input title="Personnel Code"
                                value={personnelCode}
                                setValueFunc={setPersonnelCode}/>
                <EditCard.Input title="Unit"
                                value={unit}
                                setValueFunc={setUnit}/>
                <EditCard.Input title="Manager Name"
                                value={managerName}
                                setValueFunc={setManagerName}/>
                <EditCard.Input title="Manager Email"
                                value={managerEmail}
                                setValueFunc={setManagerEmail}/>
            </EditCard>
            <Container>
            <span className="text-muted">* It's highly recommended to provide work emails for the corresponding fields. Email addresses are used to inform the communications between SahaBee and the company (mainly by CCing them).</span>
            </Container>
        </>
    )
}
