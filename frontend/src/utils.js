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
}
const utils = new Utils()
export default utils
