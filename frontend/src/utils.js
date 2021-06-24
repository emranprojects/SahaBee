import moment from "jalali-moment";

class Utils {
    isLoggedIn() {
        const token = localStorage.getItem('token')
        return !!token
    }

    setLoggedIn(token){
        localStorage.setItem('token', token)
    }

    logout() {
        localStorage.removeItem('token')
    }

    get _token() {
        return localStorage.getItem('token')
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

    async post(url, body) {
        const result = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        })
        return result
    }

    formatDateTime(datetime){
        return moment(datetime).format("jYYYY-jMM-jDD HH:mm:ss")
    }
}
const utils = new Utils()
export default utils
