import React from "react";
import {Button, Container, Jumbotron} from "react-bootstrap";

export default function TermsOfService() {
    return <>
        <Jumbotron>
            <Container>
                <h1 className="text-info">SahaBee Terms of Service</h1>
                <span className="text-justify">
                By registering at and continuing to use SahaBee service, you agree that:<br/>
                <ul>
                    <li>
                        SahaBee is a free and open-source facility to help people manage their work time-sheets and hence is not responsible for any data-loss, data-corruption, unavailability, leakage, etc. while trying it's best to avoid such failures.
                    </li>
                    <li>
                        SahaBee can use the statistical data of the users in any way.
                    </li>
                    <li>
                        Currently, roll calling is protected and available only to the authenticated users, and just for self data manipulation. But, download of timesheet files are not restricted; i.e. unauthorized users can download them.
                    </li>
                    <li>
                        The terms of service may change on the future; continuing to use SahaBee (by keeping account or usage) means agreeing on such changes too.
                    </li>
                </ul>
            </span>
            </Container>
        </Jumbotron>
    </>
}
