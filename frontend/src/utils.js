import React from "react";
import moment from "jalali-moment";
import {useEffect} from "react";


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

    async request(method, url, authorized, body = undefined) {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        if (authorized)
            headers['Authorization'] = `Token ${this._token}`

        const resp = await fetch(url, {
            method,
            headers,
            body: body !== undefined ? JSON.stringify(body) : undefined
        })
        return resp
    }

    async get(url, authorized = true) {
        return await this.request('GET', url, authorized)
    }

    async post(url, body = {}, authorized = true) {
        return await this.request('POST', url, authorized, body)
    }

    async put(url, body = {}) {
        return await this.request('PUT', url, true, body)
    }

    async delete(url) {
        return this.request('DELETE',url,true)
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

    isDev(){
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
