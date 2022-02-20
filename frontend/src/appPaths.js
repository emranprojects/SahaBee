class AppPaths {
    get login() {
        return "/login"
    }
    get oAuthLogin() {
        return "/oauth-login"
    }
    get register() {
        return "/register"
    }
    get dashboard() {
        return "/dashboard"
    }
    get termsOfService() {
        return "/terms-of-service"
    }
    get userProfile(){
        return "/user-profile"
    }
    get addRollout(){
        return "/add-rollout"
    }
    get usersCheckinStatus(){
        return "/users-checkin-status"
    }
}

const appPaths = new AppPaths()

export default appPaths