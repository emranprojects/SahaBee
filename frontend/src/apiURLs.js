class ApiUrls {
    get BASE_URL() {
        return window.AppConfig.API_BASE_URL
    }
    get login() {
        return `${this.BASE_URL}/api-token-auth/`
    }
    get register() {
        return `${this.BASE_URL}/users/register/`
    }
    get rollouts() {
        return `${this.BASE_URL}/rollouts/`
    }
}

const apiURLs = new ApiUrls()

export default apiURLs