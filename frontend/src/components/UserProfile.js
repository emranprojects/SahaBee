import React, {useState} from "react";
import utils from "../utils";
import {Redirect} from "react-router-dom";
import appPaths from "../appPaths";
import {Col, FormControl, InputGroup} from "react-bootstrap";
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
    const [loading, setLoading] = useState(true)
    const [authorized, setAuthorized] = useState(true)


    if (!utils.isLoggedIn() || !authorized)
        return <Redirect to={appPaths.login}/>

    utils.useEffectAsync(fetchUser, [])

    async function fetchUser() {
        const resp = await utils.get(apiURLs.selfUser)

        switch (resp.status) {
            case 200:
                const user = await resp.json()
                inflateStates(user)
                setLoading(false)
                break
            case 401:
                toast.error("Not logged in!")
                setAuthorized(false)
                break
            default:
                const txt = await resp.text()
                console.error(txt)
                toast.error(`Unexpected status code (${resp.status}): ${(txt.substr(0, 100))}`)
                break
        }
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
                manager_name: managerName
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
        switch (resp.status) {
            case 200:
                toast.success("Info updated successfully!")
                break
            case 400:
                // TODO: Nice form errors
                toast.error(await resp.text())
                break
            default:
                toast.error(`Unexpected status code (${resp.status}): ${await resp.text()}`)
        }
    }

    return (
        <EditCard title="Profile Information" onSave={save} loading={loading}>
            <Input title="@"
                   value={username}
                   setValueFunc={setUsername}/>
            <Input title="Email"
                   value={email}
                   setValueFunc={setEmail}/>
            <Input title="Firstname"
                   value={firstname}
                   setValueFunc={setFirstname}/>
            <Input title="Lastname"
                   value={lastname}
                   setValueFunc={setLastname}/>
            <Input title="Personnel Code"
                   value={personnelCode}
                   setValueFunc={setPersonnelCode}/>
            <Input title="Unit"
                   value={unit}
                   setValueFunc={setUnit}/>
            <Input title="Manager Name"
                   value={managerName}
                   setValueFunc={setManagerName}/>
        </EditCard>
    )
}

function Input({title, value, setValueFunc}) {
    return (
        <Col md={4} className="pt-2">
            <InputGroup>
                <InputGroup.Prepend>
                    <InputGroup.Text>
                        {title}
                    </InputGroup.Text>
                </InputGroup.Prepend>
                <FormControl
                    value={value}
                    onChange={e => setValueFunc(e.target.value)}/>
            </InputGroup>
        </Col>
    )
}
