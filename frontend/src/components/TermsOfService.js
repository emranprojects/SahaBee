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
                        As a facility, SahaBee may try to send the timesheets to the administrative manager, periodically. However, it's the users responsibility to make sure the times are received and correct, finally.
                    </li>
                    <li>
                        SahaBee emails the timesheets <b>from</b> the user's email address. So it looks like the user himself has sent the timesheet.
                        It's a facility for the management-side to distinguish users more easily.<br/>
                        Absolutely, it's explained in the message body that the email is sent automatically by SahaBee.
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
