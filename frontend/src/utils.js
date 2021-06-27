import moment from "jalali-moment";


export const DateFormat = Object.freeze({
    DATE: 1,
    TIME: 2,
})

class Utils {
    isLoggedIn() {
        const token = localStorage.getItem('token')
        return !!token
    }

    setLoggedIn(username, token){
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

    async get(url) {
        const result = await fetch(url, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `Token ${this._token}`
            },
        })
        return result
    }

    async post(url, body = {}, authorized = true) {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

        if (authorized)
            headers['Authorization'] = `Token ${this._token}`

        const result = await fetch(url, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(body)
        })
        return result
    }

    async delete(url, ) {
        const result = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': `Token ${this._token}`
            },
        })
        return result
    }

    formatDateTime(datetime, dateFormat = DateFormat.DATE | DateFormat.TIME){
        let format
        switch (dateFormat){
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
}
const utils = new Utils()
export default utils
