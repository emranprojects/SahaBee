export default {
    isLoggedIn: () => {
        const token = localStorage.getItem('token')
        return !!token
    },
    post: async (url, body) => {
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