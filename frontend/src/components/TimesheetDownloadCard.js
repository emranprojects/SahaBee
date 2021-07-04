import React, {useState} from "react";
import {Card, Col, FormControl, InputGroup, Row} from "react-bootstrap";
import moment from "jalali-moment";
import {toast} from "react-toastify";
import apiURLs from "../apiURLs";
import utils from "../utils";
import AuthenticatedLink from "./AuthenticatedLink";
import {Redirect} from "react-router-dom";
import appPaths from "../appPaths";

export default function TimesheetDownloadCard({lastAddedRolloutId}) {
    const YEAR_MIN = 1300
    const YEAR_MAX = 2000
    const MONTH_MIN = 1
    const MONTH_MAX = 12

    const now = moment()
    const [year, setYear] = useState(now.jYear())
    const [month, setMonth] = useState(now.jMonth() + 1)
    const [tokenInvalid, setTokenInvalid] = useState(false)

    if (!utils.isLoggedIn() || tokenInvalid)
        return <Redirect to={appPaths.login}/>

    function validateDownloadArgs() {
        if (year < YEAR_MIN || year > YEAR_MAX) {
            toast.error("Invalid year!")
            return false
        }
        if (month < MONTH_MIN || month > MONTH_MAX) {
            toast.error("Invalid month!")
            return false
        }
        return true
    }

    function onDownloadError401() {
        toast.error("Not logged in!")
        setTokenInvalid(true)
    }

    return <Card>
        <Card.Header>Download time-sheet</Card.Header>
        <Card.Body>
            <Row>
                <Col md={2}>
                    <InputGroup>
                        <InputGroup.Prepend>
                            <InputGroup.Text>
                                Year
                            </InputGroup.Text>
                        </InputGroup.Prepend>
                        <FormControl type="number"
                                     min={YEAR_MIN}
                                     max={YEAR_MAX}
                                     value={year}
                                     onChange={e => setYear(Number(e.target.value))}/>
                    </InputGroup>
                </Col>
                <Col md={2}>
                    <InputGroup>
                        <InputGroup.Prepend>
                            <InputGroup.Text>
                                Month
                            </InputGroup.Text>
                        </InputGroup.Prepend>
                        <FormControl type="number"
                                     min={MONTH_MIN}
                                     max={MONTH_MAX}
                                     value={month}
                                     onChange={e => setMonth(Number(e.target.value))}/>
                    </InputGroup>
                </Col>
                <Col>
                    <AuthenticatedLink url={`${apiURLs.timesheetDownload(utils.username, year, month)}`}
                                       className="btn btn-info"
                                       filename={`timesheet-${year}-${month}`}
                                       validateFunc={validateDownloadArgs}
                                       refreshArg={lastAddedRolloutId}
                                       onError401={onDownloadError401}
                    >
                        Download!
                    </AuthenticatedLink>
                </Col>
            </Row>
        </Card.Body>
    </Card>
}
