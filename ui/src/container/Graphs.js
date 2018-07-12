
import React, { Component } from 'react'
import Resume from '../ui/Resume';
import Licitacoes from "../ui/Licitacoes"
import Companies from '../ui/Companies';
export default class Graphs extends Component {

    render() {
        return (
            <div style={{ paddingTop: "6%" }} >
                <Resume />
                <Licitacoes />
                <Companies />
            </div>
        );
    }
}