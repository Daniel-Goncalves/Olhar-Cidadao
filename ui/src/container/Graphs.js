import React, { Component } from 'react'
import Resume from '../ui/Resume';

export default class Graphs extends Component {

    render() {
        return (
            <div style={{paddingTop: "10%"}} >
                <h1>{this.props.params.id}</h1>
                <Resume />
                
            </div>
        );
    }
}