class ApiUrls {
    get BASE_URL() {
        return "http://localhost:8000"
    }
    get login() {
        return `${this.BASE_URL}/api-token-auth/`
    }
}

const apiURLs = new ApiUrls()

export default apiURLs