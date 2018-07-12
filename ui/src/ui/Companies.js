import React, { Component } from 'react'


export default class Companies extends Component {
    constructor() {
        super();
        var str = window.location.href;
        str = str.split("/");
        this.state = {
            id: '',
            instituicao: str[5],
            datatable: [],

        };
    }
    Comparator(a, b) {
        if (a[1] < b[1])
            return -1;
        else if (a[1] > b[1])
            return 1;
        else if (a[2] < b[2])
            return -1;
        else if (a[2] > b[2])
            return 1;
        return 0;
    }

    componentDidMount() {
        fetch('http://localhost:8080/get_winner_companies', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                specific_instituition: this.state.instituicao
            })
        }).then(result => {
            return result.json();
        })
            .then(result => {
                console.log(result);
                let arr = Object.values(result['Winner companies']);
                let companies = [];
                arr.map((empresas, index) => {
                    companies[index] = [empresas.nome_empresa, empresas.number_of_wins, empresas.total_value];
                });
                companies.sort(this.Comparator);
                companies.reverse();
                this.setState({
                    datatable: companies,
                });

            });
    }
    tigger() {
        fetch('http://localhost:8080/get_winner_companies', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                maximum_number_of_wins_same_bidding: 2  
            })
        }).then(result => {
            return result.json();
        })
            .then(result => {
                console.log(result);
            });
    }
    render() {
        return (
            <div>
                <section id="companies">
                    <div style={{ paddingTop: "20px", paddingLeft: "30px" }}>
                        <div className="row">
                            <h2 className="display-4">Empresa<br /><p className="lead">Neste tópico você pode ver informações detalhadas sobre as empresas<br /> e também filtrar essas informações</p></h2>
                        </div>
                        <div style={{ marginTop: "20px", marginBottom: "20px", marginLeft: '20px' }} className='row'>
                            <div>
                                Ordernar por
                                <div style={{ marginLeft: '15px', marginRight: '20px', marginTop: '4px' }} className="btn-group btn-group-toggle" data-toggle="buttons">
                                    <label className="btn btn-secondary active">
                                        <input type="radio" name="options" id="option1" autocomplete="off" checked /> Vitórias
                                    </label>
                                    <label className="btn btn-secondary">
                                        <input type="radio" name="options" id="option2" autocomplete="off" /> Valores
                                    </label>
                                    <label className="btn btn-secondary">
                                        <input type="radio" name="options" id="option3" autocomplete="off" /> Empresas
                                    </label>
                                </div>
                            </div>
                            <div style={{ marginLeft: '15px', marginRight: '15px' }} className="col-sm-3 my-1">
                                <label className="sr-only" for="inlineFormInputGroupUsername">Valor mínimo</label>
                                <div className="input-group">
                                    <div className="input-group-prepend">
                                        <div className="input-group-text">Valores mínimos</div>
                                    </div>
                                    <input type="number" className="form-control" id="inlineFormInputGroupUsername" placeholder="" />
                                </div>
                            </div>
                            <div style={{ marginLeft: '15px', marginRight: '15px' }} className="col-sm-3 my-1">
                                <label className="sr-only" for="inlineFormInputGroupUsername">Mínimo de vitórias</label>
                                <div className="input-group">
                                    <div className="input-group-prepend">
                                        <div className="input-group-text">Mínimo de vitórias</div>
                                    </div>
                                    <input type="number" className="form-control" id="inlineFormInputGroupUsername" placeholder="" />
                                </div>
                            </div>
                            <button onClick={this.tigger} type="button" className="btn btn-outline-dark">Filtrar</button>
                        </div>
                        <div className="row">
                            <table className='col-6' className="table">
                                <thead>
                                    <tr>
                                        <th scope="col">Empresa</th>
                                        <th scope="col">Vitórias</th>
                                        <th scope="col">Valor ganho</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {this.state.datatable.map(empresa =>
                                        <tr>
                                            <td>{empresa[0]}</td>
                                            <td>{empresa[1]}</td>
                                            <td>R$ {empresa[2].toLocaleString()}</td>
                                        </tr>)}
                                </tbody>
                            </table>
                        </div>

                    </div>
                </section>
            </div >
        );
    }
}
