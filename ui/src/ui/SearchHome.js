import React, { Component } from 'react'

export default class SearchHome extends Component {

    render() {
        return (
            <header id="searchBar" >
                <div className="container text-center">
                    <h1>Bem vindo ao Olhar Cidadão</h1>
                    <p className="lead">Aqui você pode consultar dados de licitações de Municípios e Universidades!</p>
                    <div style={{ width: "800px", margin: "auto" }} className="input-group mb-3">
                        <input type="text" className="form-control" placeholder="Pesquise aqui!" aria-label="Pesquise aqui!" aria-describedby="basic-addon2" />
                        <div className="input-group-append">
                            <a href='graphs.html' className="btn btn-outline-secondary" type="button">Buscar</a>
                        </div>
                    </div>

                </div>
            </header>
        );
    }
}