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
    rollout(id){
        return `${this.rollouts}${id}/`
    }
    timesheetDownload(username, year, month){
        return `${this.BASE_URL}/${username}/${year}/${month}/timesheet.xlsx`
    }
}

const apiURLs = new ApiUrls()

export default apiURLs