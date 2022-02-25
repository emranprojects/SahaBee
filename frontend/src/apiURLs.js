class ApiUrls {
    get BASE_URL() {
        return window.AppConfig.API_BASE_URL
    }
    get login() {
        return `${this.BASE_URL}/api-token-auth/`
    }
    get _users() {
        return `${this.BASE_URL}/users/`
    }
    get googleUserLogin() {
        return `${this._users}google-user-login/`
    }
    get selfUser() {
        return `${this._users}self/`
    }
    get allUsers() {
        return `${this._users}all/`
    }
    get usersCheckinStatuses() {
        return `${this._users}checkin-statuses/`
    }
    get register() {
        return `${this._users}register/`
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
    get apiDocs(){
        return `${this.BASE_URL}/docs/`
    }
}

const apiURLs = new ApiUrls()

export default apiURLs