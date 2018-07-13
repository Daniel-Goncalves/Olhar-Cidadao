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
    Wins(a, b) {
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
    Values(a, b) {
        if (a[2] < b[2])
            return -1;
        else if (a[2] > b[2])
            return 1;
        else if (a[1] < b[1])
            return -1;
        else if (a[1] > b[1])
            return 1;
        return 0;
    }
    Names(a, b) {
        if (a[0] < b[0])
            return -1;
        else if (a[0] > b[0])
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
                companies.sort(this.Wins);
                companies.reverse();
                this.setState({
                    datatable: companies,
                });

            });
    }
    tigger(aux) {
        let option = aux.target.value;
        let payload = this.state.datatable;
        if (option === '1') {
            payload.sort(this.Wins);
            payload.reverse();
        }
        else if (option === '2') {
            payload.sort(this.Values);
            payload.reverse();
        }
        else if (option === '3')
            payload.sort(this.Names);

        this.setState({
            datatable: payload
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
                        <div style={{ marginTop: "20px", marginBottom: "20px" }} className='row'>
                            <div>
                                Ordernar por
                                <div style={{ marginLeft: '15px', marginRight: '20px', marginTop: '4px' }}>
                                    <button value='1' style={{ margin: '3px' }} className="btn btn-dark" onClick={this.tigger.bind(this)} type="radio" name="options" id="option1" autocomplete="off" checked>Vitórias</button>
                                    <button value='2' style={{ margin: '3px' }} className="btn btn-dark" onClick={this.tigger.bind(this)} type="radio" name="options" id="option2" autocomplete="off"> Valores </button>
                                    <button value='3' style={{ margin: '3px' }} className="btn btn-dark" onClick={this.tigger.bind(this)} type="radio" name="options" id="option3" autocomplete="off"> Empresas</button>
                                </div>
                            </div>
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
