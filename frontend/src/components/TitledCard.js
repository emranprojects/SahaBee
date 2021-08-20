import Card from "react-bootstrap/Card";
import Row from "react-bootstrap/Row";
import {Spinner} from "react-bootstrap";

export default function TitledCard({title, loading = false, children}) {
    return (
        <Card>
            <Card.Header>
                <Row>
                    <h5 className="ml-2">{title}</h5>
                    {loading ?
                        <Spinner animation="border" variant="info" className="ml-auto mr-2"/> : ""
                    }
                </Row>
            </Card.Header>
            {children}
        </Card>
    )
}