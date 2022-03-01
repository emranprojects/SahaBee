import React, {useState} from "react";
import utils from "../utils";
import {Redirect} from "react-router-dom";
import appPaths from "../appPaths";
import {Button, Container, Form, FormControl, InputGroup, Row} from "react-bootstrap";
import apiURLs from "../apiURLs";
import {toast} from "react-toastify";
import EditCard from "../components/EditCard";
import TitledCard from "../components/TitledCard";
import Modal from 'react-modal';

export default function UserProfile() {
    const [userId, setUserId] = useState()
    const [userDetailId, setUserDetailId] = useState()
    const [username, setUsername] = useState("")
    const [workEmail, setWorkEmail] = useState("")
    const [firstname, setFirstname] = useState("")
    const [lastname, setLastname] = useState("")
    const [personnelCode, setPersonnelCode] = useState("")
    const [unit, setUnit] = useState("")
    const [managerName, setManagerName] = useState("")
    const [managerEmail, setManagerEmail] = useState("")
    const [loading, setLoading] = useState(true)
    const [authorized, setAuthorized] = useState(true)
    const [enableTimesheetAutoSend, setEnableTimesheetAutoSend] = useState(false)

    Modal.setAppElement('#root')
    utils.useEffectAsync(fetchUser, [])

    if (!utils.isLoggedIn() || !authorized)
        return <Redirect to={appPaths.login}/>

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
        setFirstname(user.first_name)
        setLastname(user.last_name)
        setWorkEmail(user.detail.work_email)
        setUserDetailId(user.detail.id)
        setPersonnelCode(user.detail.personnel_code)
        setUnit(user.detail.unit)
        setManagerName(user.detail.manager_name)
        setManagerEmail(user.detail.manager_email)
        setEnableTimesheetAutoSend(user.detail.enable_timesheet_auto_send)
    }

    function getUserFromStates() {
        return {
            id: userId,
            username,
            first_name: firstname,
            last_name: lastname,
            detail: {
                work_email: workEmail,
                id: userDetailId,
                personnel_code: personnelCode,
                unit,
                manager_name: managerName,
                manager_email: managerEmail,
                enable_timesheet_auto_send: enableTimesheetAutoSend
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

    const footerHint = <span className="text-muted">
        * It's highly recommended to provide work-domain emails for the corresponding fields. Email addresses are used to inform the communications between SahaBee and the company (mainly by CCing them).<br/>
        ** Active timesheets are the ones that have been filled recently.
    </span>

    return (
        <>
            <EditCard title="Profile Information"
                      onSave={save} loading={loading}
                      footer={footerHint}>
                <EditCard.Input title="@"
                                value={username}
                                setValueFunc={setUsername}/>
                <EditCard.Input title="Work Email*"
                                value={workEmail}
                                setValueFunc={setWorkEmail}/>
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
                <EditCard.Input title="Manager Email*"
                                value={managerEmail}
                                setValueFunc={setManagerEmail}/>
                <EditCard.InputCell>
                    <Form.Check type="switch"
                                id={Math.random()} // Workaround: https://stackoverflow.com/questions/57748179
                                label={<span>Enable auto-sending of <b>active**</b> timesheets to the office.</span>}
                                checked={enableTimesheetAutoSend}
                                onChange={e => setEnableTimesheetAutoSend(e.target.checked)}
                    />
                </EditCard.InputCell>
            </EditCard>
            <DangerZone username={username} onNotAuthorized={() => setAuthorized(false)}/>
        </>
    )
}

function DangerZone({username, onNotAuthorized}) {
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false)
    const [usernameInputValue, setUsernameInputValue] = useState("")

    function closeModal() {
        setIsDeleteModalOpen(false)
        setUsernameInputValue("")
    }

    async function deleteAccount() {
        const resp = await utils.delete(apiURLs.selfUser,
            () => {
                toast.error("Not logged in! Please login again!")
                onNotAuthorized()
            })
        if (resp.status === 200) {
            toast.success("Account deleted successfully!")
            onNotAuthorized()
        } else
            toast.error(`Unexpected status code: ${resp.status}`)
    }

    return <Container>
        <Row className="mb-5"/>
        <TitledCard title="Danger Zone">
                    <span className="m-3">
                        To delete your account and its data click on the below button.<br/>
                        Note that this action can not be undone!
                    </span>
            <Button className="btn-danger" onClick={() => setIsDeleteModalOpen(true)}>Delete Account</Button>
            <Modal
                isOpen={isDeleteModalOpen}
                onRequestClose={closeModal}
                contentLabel="Delete Account"
                style={{
                    content: {
                        top: '50%',
                        left: '50%',
                        right: 'auto',
                        bottom: 'auto',
                        maxWidth: '400pt',
                        marginRight: '-50%',
                        transform: 'translate(-50%, -50%)',
                    },
                }}
            >
                <b>This action can not be undone!</b><br/>
                If you're sure about deleting the account and all its data,
                please enter your username and press delete button.
                <InputGroup>
                    <InputGroup.Prepend>
                        <InputGroup.Text>
                            Your Username
                        </InputGroup.Text>
                    </InputGroup.Prepend>
                    <FormControl
                        value={usernameInputValue}
                        onChange={e => setUsernameInputValue(e.target.value)}/>
                </InputGroup>
                <Button className="w-50 mt-3 btn-secondary"
                        onClick={closeModal}>Cancel</Button>
                <Button className="w-25 btn-danger mt-3 float-right"
                        disabled={usernameInputValue !== username}
                        onClick={deleteAccount}>
                    Delete
                </Button>
            </Modal>
        </TitledCard>
    </Container>
}
