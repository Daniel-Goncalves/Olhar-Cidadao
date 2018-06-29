
import React, { Component } from 'react'
import Resume from '../ui/Resume';
import Licitacoes from "../ui/Licitacoes"
export default class Graphs extends Component {

    render() {
        return (
            <div style={{ paddingTop: "6%" }} >
                <Resume {...this.props} />
                <Licitacoes />
            </div>
        );
    }
}