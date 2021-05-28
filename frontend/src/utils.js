export default {
    isLoggedIn: () => {
        const token = localStorage.getItem('token')
        return !!token
    }
}