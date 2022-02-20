import React, {useState} from "react";
import EditCard from "../components/EditCard";
import moment from "jalali-moment";
import utils, {DateFormat} from "../utils";
import apiURLs from "../apiURLs";
import {toast} from "react-toastify";
import {Redirect} from "react-router-dom";
import appPaths from "../appPaths";
import {Calendar} from "react-multi-date-picker";
import persian from "react-date-object/calendars/persian"
import persian_fa from "react-date-object/locales/persian_fa"

export default function RolloutEditPage({rolloutId = null}) {
    const [loading, setLoading] = useState(!!rolloutId)
    const [date, setDate] = useState(moment())
    const [timeStr, setTimeStr] = useState(utils.formatDateTime(moment(), DateFormat.TIME))
    const [tokenInvalid, setTokenInvalid] = useState(false)
    const [saveSucceeded, setSaveSucceeded] = useState(false)

    if (!utils.isLoggedIn() || tokenInvalid)
        return <Redirect to={appPaths.login}/>
    if (saveSucceeded)
        return <Redirect to={appPaths.dashboard}/>

    async function save() {
        const time = moment(timeStr, 'HH:mm:ss')
        if (!time.isValid()) {
            toast.error("Invalid time!")
            return
        }
        date.set({
            hour: time.hour(),
            minute: time.minute(),
            second: time.second()
        })
        const resp = await utils.post(apiURLs.rollouts, {time: date})
        if (resp.status === 201) {
            const rollout = await resp.json()
            toast.success(<span>Rollout Saved!<br/>{utils.formatDateTime(rollout.time)}</span>)
            setSaveSucceeded(true)
        }
    }

    return (
        <EditCard title={rolloutId ? "Edit Rollout" : "Add new Rollout"}
                  loading={loading} onSave={save}>
            <Calendar className="ml-4"
                      onChange={v => setDate(moment(`${v.year}-${v.month.number}-${v.day}`, 'jYYYY-jMM-jDD'))}
                      calendar={persian}
                      locale={persian_fa}
            />
            <EditCard.Input title="Time"
                            className="mt-2"
                            value={timeStr}
                            setValueFunc={setTimeStr}/>
        </EditCard>
    )
}