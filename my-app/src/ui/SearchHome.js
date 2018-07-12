import React, { Component } from 'react'
import { Link } from 'react-router'

var Typeaheads = require('react-bootstrap-typeahead').Typeahead; // CommonJS
export default class SearchHome extends Component {
    constructor() {
        super();
        this.state = {
            id: '',
            instituicoes: false, 
        };
        fetch("http://172.16.20.20:8080/get_instituicoes")
            .then(result=> {
		console.log(result)
                //console.log(result.json())
                return result.json();
            })
            .then(result=>{

                this.setState({instituicoes: result.instituicoes});
                
            });
    }


    _handleKeyPress = (e) => {
        if (e.key === 'Enter' && this.state.id !== '') {
            document.getElementById("buttonpress").click();
        }
    }
    handle(str) {
        this.setState({
            id: str
        })
    }
    render() {
        return (
            <header id="searchBar" >
                <div className="container text-center">
                    <h1>Bem vindo ao Olhar Cidadão</h1>
                    <div>
                    </div>
                    <p className="lead">Aqui você pode consultar dados de licitações de Municípios e Universidades!</p>
                    <div style={{ width: "800px", margin: "auto" }} className="input-group mb-3">
                            <Typeaheads
                                style={{ width: "800px" }}
                                id='type'
                                onChange={this.handle.bind(this)}
                                onkeypress={this._handleKeyPress}
                                type="text"
                                placeholder="Pesquise aqui!"
                                aria-label="Pesquise aqui!"
                                aria-describedby="basic-addon2"
                                options={this.state.instituicoes || ['']}
                                maxVisible={2}
                            />
                        <div className="input-group-append">
                            <Link to={`/graphs/${this.state.id}`} onClick={this.handle.bind(this)} id='buttonpress' className="btn btn-outline-secondary">Buscar</Link>
                        </div>        


                    </div>

                </div>
            </header>
        );
    }
}
