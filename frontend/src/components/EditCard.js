import {Button, Card, Col, Container, FormControl, InputGroup, Row, Spinner} from "react-bootstrap";
import React from "react";
import TitledCard from "./TitledCard";

export default function EditCard({loading, title, children, onSave = () => undefined, footer = ""}) {
    return (
        <Container>
            <Row className="mb-5"/>
            <TitledCard title={title} loading={loading}>
                <Card.Body>
                    <Row>
                        {children}
                    </Row>
                </Card.Body>
                <Card.Footer>
                    <Row>
                        <Col md={10}>
                            {footer}
                        </Col>
                        <Col md={2}>
                            <Button variant="info" className="pr-5 pl-5 float-right" onClick={onSave}>Save</Button>
                        </Col>
                    </Row>
                </Card.Footer>
            </TitledCard>
        </Container>
    )
}

EditCard.InputCell = function ({children}) {
    return (
        <Col md={4} className="pt-2">
            {children}
        </Col>
    )
}

EditCard.Input = function ({title, value, setValueFunc}) {
    return (
        <EditCard.InputCell>
            <InputGroup>
                <InputGroup.Prepend>
                    <InputGroup.Text>
                        {title}
                    </InputGroup.Text>
                </InputGroup.Prepend>
                <FormControl
                    value={value}
                    onChange={e => setValueFunc(e.target.value)}/>
            </InputGroup>
        </EditCard.InputCell>
    )
}