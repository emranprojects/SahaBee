import React from "react";
import moment from "jalali-moment";
import {useEffect} from "react";
import {toast} from "react-toastify";


export const DateFormat = Object.freeze({
    DATE: 1,
    TIME: 2,
})

class Utils {
    isLoggedIn() {
        const token = localStorage.getItem('token')
        return !!token
    }

    setLoggedIn(username, token) {
        localStorage.setItem('username', username)
        localStorage.setItem('token', token)
    }

    logout() {
        localStorage.removeItem('username')
        localStorage.removeItem('token')
    }

    get _token() {
        return localStorage.getItem('token')
    }

    get username() {
        return localStorage.getItem('username')
    }

    async request(method, url, onError401 = () => undefined, authorized = false, body = undefined) {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        if (authorized)
            headers['Authorization'] = `Token ${this._token}`

        try {
            const resp = await fetch(url, {
                method,
                headers,
                body: body !== undefined ? JSON.stringify(body) : undefined
            })
            switch (resp.status) {
                case 400:
                    const errors = await resp.json()
                    let errorMsg = ""
                    for (let title in errors)
                        errorMsg += `${title}: ${errors[title]}\n`
                    toast.error(errorMsg)
                    break
                case 401:
                    toast.error("Not logged in!")
                    onError401()
                    break
            }
            return resp
        } catch (e) {
            toast.error("Failed to connect to server!")
            console.log(e)
            return {
                status: -1,
                text: async () => "Connection failed!",
                json: async () => ({})
            }
        }
    }

    async get(url, onError401 = () => undefined, authorized = true) {
        return await this.request('GET', url, onError401, authorized, undefined)
    }

    async post(url, body = {}, onError401 = () => undefined, authorized = true) {
        return await this.request('POST', url, onError401, authorized, body)
    }

    async put(url, body = {}, onError401 = () => undefined) {
        return await this.request('PUT', url,onError401, true, body)
    }

    async delete(url, onError401 = () => undefined) {
        return this.request('DELETE', url, onError401, true)
    }

    formatDateTime(datetime, dateFormat = DateFormat.DATE | DateFormat.TIME) {
        let format
        switch (dateFormat) {
            case DateFormat.DATE:
                format = "jYYYY-jMM-jDD"
                break
            case DateFormat.TIME:
                format = "HH:mm:ss"
                break
            case DateFormat.DATE | DateFormat.TIME:
                format = "jYYYY-jMM-jDD HH:mm:ss"
                break
            default:
                throw Error(`Unknown DateFormat! (${dateFormat})`)
        }
        return moment(datetime).format(format)
    }

    useEffectAsync(asyncFunc, deps = [], thisArg = this) {
        _useEffectAsync.apply(this, [asyncFunc, deps, thisArg])
    }

    isDev() {
        return !process.env.NODE_ENV || process.env.NODE_ENV === 'development'
    }
}

function _useEffectAsync(asyncFunc, deps, thisArg) {
    useEffect(() => {
        asyncFunc.apply(thisArg)
    }, deps)
}

const utils = new Utils()
export default utils
