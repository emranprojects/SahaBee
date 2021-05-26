import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";
import React from "react";
import {Col} from "react-bootstrap";

export function HCenter({md, children}) {
    if (md > 12)
        throw Error("md can not be grater that 12")
    if (md % 2 === 1)
        md++
    const margin = (12 - md) / 2;
    if (margin === 0)
        return children
    return (
        <Container fluid>
            <Row>
                <Col md={margin}/>
                <Col md={md}>{children}</Col>
                <Col md={margin}/>
            </Row>
        </Container>
    );
}