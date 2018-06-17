import React, { Component } from 'react'
import Resume from '../ui/Resume';
import Licitacoes from "../ui/Licitacoes"
export default class Graphs extends Component {
    //<h1>{this.props.params.id}</h1>
    render() {
        return (
            <div style={{paddingTop: "10%"}} >
                <Resume />
                <Licitacoes />
            </div>
        );
    }
}