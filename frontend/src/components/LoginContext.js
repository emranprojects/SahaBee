import React from "react";

const LoginContext = React.createContext({
    isLoggedIn: false,
    setIsLoggedIn: isLoggedIn => undefined
})

export default LoginContext