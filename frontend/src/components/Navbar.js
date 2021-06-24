import appPaths from "../appPaths";
import {Navbar as BootstrapNavbar} from "react-bootstrap";
import utils from "../utils";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome'
import {faSignOutAlt} from '@fortawesome/free-solid-svg-icons'

export default function Navbar({isLoggedIn}) {
    return (
        <BootstrapNavbar className="nav-bar" bg="dark" expand="lg">
            <BootstrapNavbar.Brand href="/" className="text-white">SahaBee</BootstrapNavbar.Brand>
            {isLoggedIn ? <>
                    <a href={appPaths.dashboard} className="btn btn-dark">Dashboard</a>
                    <a href="/" className="btn btn-dark" onClick={utils.logout}>
                        <abbr title="Logout"><FontAwesomeIcon icon={faSignOutAlt} /></abbr>
                    </a>
                </> :
                <a href={appPaths.login} className="btn btn-dark">Login</a>
            }
        </BootstrapNavbar>
    )
}
