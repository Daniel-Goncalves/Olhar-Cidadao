import React, { Component } from 'react'
import { Link } from 'react-router'

export default class SearchHome extends Component {
    constructor() {
        super();
        this.state = {
            data: '',
        }
    }
    _handleKeyPress = (e) => {
        if (e.key === 'Enter' && this.state.data !== '') {
            document.getElementById("buttonpress").click();
        }
    }
    handle(event) {
        this.setState({
            data: event.target.value
        })
    }
    render() {
        return (
            <header id="searchBar" >
                <div className="container text-center">
                    <h1>Bem vindo ao Olhar Cidadão</h1>
                    <p className="lead">Aqui você pode consultar dados de licitações de Municípios e Universidades!</p>
                    <div style={{ width: "800px", margin: "auto" }} className="input-group mb-3">
                        <input onChange={this.handle.bind(this)} onKeyPress={this._handleKeyPress} type="text" className="form-control" placeholder="Pesquise aqui!" aria-label="Pesquise aqui!" aria-describedby="basic-addon2" />
                        <div className="input-group-append">
                            <Link to={`/graphs/${this.state.data}`} id='buttonpress' className="btn btn-outline-secondary">Buscar</Link>
                        </div>
                    </div>

                </div>
            </header>
        );
    }
}