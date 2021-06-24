import appPaths from "../appPaths";
import {Navbar as BootstrapNavbar} from "react-bootstrap";
import utils from "../utils";

export default function Navbar({isLoggedIn}) {
    return (
        <BootstrapNavbar className="nav-bar" bg="dark" expand="lg">
            <BootstrapNavbar.Brand href="/" className="text-white">SahaBee</BootstrapNavbar.Brand>
            {isLoggedIn ? <>
                    <a href={appPaths.dashboard} className="btn btn-dark">Dashboard</a>
                    <a href="/" className="btn btn-dark" onClick={utils.logout}>Logout</a>
                </> :
                <a href={appPaths.login} className="btn btn-dark">Login</a>
            }
        </BootstrapNavbar>
    )
}
