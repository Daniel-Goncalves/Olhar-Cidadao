import React, { Component } from 'react'

var descEmpresas = {};
export default class Resume extends Component {
    constructor() {
        super();
        var str = window.location.href;
        str = str.split("/");
        this.state = {
            processos: [],
            instituicao: str[5],
            licitacoes: [],
            suspects: [],
        };
    }
    componentDidMount() {
        let array = [];

        fetch("http://localhost:9000/get_winner_companies")
            .then(result => {
                //console.log(result.json())
                return result.json();
            })
            .then(result => {
                this.setState({ suspects: result['Winner companies'] });
                console.log(this.state.suspects);
            });

        let cont = 0;
        fetch('http://localhost:9000/get_instituicao', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                instituicao: this.state.instituicao
            })
        }).then(result => {
            return result.json();
        })
            .then(result => {
                let licitacoes = result['Licitacoes dessa Instituicao'];
                console.log(licitacoes);
                licitacoes.map(licitacao => {
                    array[cont] = licitacao.numero_processo;
                    cont++;
                })
                this.setState({
                    processos: array,
                    licitacoes: licitacoes
                })
            });
    }
    componentDidUpdate() {
        let aux = this.state.licitacoes;
        let temp = aux[0].numero_processo;
        let element = document.getElementById(temp);
        element.classList.add("active");
    }
    render() {
        const processos = this.state.processos;
        const licitacoes = this.state.licitacoes;
        const empresas = this.state.suspects;
        return (
            <section id='licitacoes'>
                <div style={{ paddingTop: "20px", paddingLeft: "30px" }}>
                    <div className="row">
                        <h2 className="display-4">Licitações</h2><br />
                    </div>
                    <div className="row" >
                        <p className="lead">Aqui você pode consultar todas as licitações do orgão pesquisado</p>
                    </div>
                </div>
                <div className="row">
                    <div style={{ textAlign: "center", width: "100%" }}>
                        <div className="dropdown">
                            <button className="btn btn-secondary dropdown-toggle" type="button" id="botao_lic" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Escolha sua Licitação!</button>
                            <div className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                                {processos.map(i => <li className="btn btn-light" data-target="#carousel_lic" data-slide-to={i.replace(/ /g, '')} style={{ cursor: "pointer" }}>{i}</li>)}
                            </div>
                        </div>
                    </div>
                </div>
                <div id="carousel_lic" className="carousel slide" data-interval="false" data-ride="carousel">
                    <ol className="carousel-indicators">
                        {processos.map(i => <li data-target="#carousel_lic" data-slide-to={i.replace(/ /g, '')}></li>)}
                    </ol>
                    <div className="carousel-inner">
                        {licitacoes.map(licitacao =>
                            <div id={licitacao.numero_processo} className="carousel-item">
                                <h2 className="col-2">{licitacao.numero_processo}</h2>
                                <table className="table">
                                    <thead>
                                        <tr>
                                            <th scope="col">Empresa</th>
                                            <th scope="col">Valor Global</th>
                                            <th scope="col">Valor Estimado</th>
                                            <th scope="col">Ata</th>
                                            <th scope="col">Vigência</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {licitacao.empresas.map(empresa =>
                                            <tr>
                                                <td><button type="button" className="btn btn-link" data-toggle="modal" data-target={"#" + empresa.nome_empresa.replace(/ /g, '')}>{empresa.nome_empresa}</button></td>
                                                <td>{empresa.valor_global} </td>
                                                <td>{empresa.valor_estimado}</td>
                                                <td>{empresa.ata}</td>
                                                <td>{empresa.vigencia}</td>
                                            </tr>)}
                                    </tbody>
                                </table>
                                <div style={{ textAlign: "center" }}>
                                    <button className="btn btn-danger" type="button" data-toggle="collapse" data-target="#comp_lic1" aria-expanded="false" aria-controls="collapseExample"
                                        style={{ marginBottom: "35px" }}>Comparações</button>

                                    <div className="collapse" id="comp_lic1">
                                        <div className="card card-body" style={{ marginBottom: "35px" }}>
                                            <div className="accordion" id="accordionExample">
                                                <div className="card">
                                                    <div className="card-header" id="headingOne">
                                                        <h5 className="mb-0">
                                                            <button className="btn btn-link" type="button" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                                                                Lote1
                                                            </button>
                                                        </h5>
                                                    </div>
                                                    <div id="collapseOne" className="collapse" aria-labelledby="headingOne" data-parent="#accordionExample">
                                                        <div className="card-body">
                                                            <table className="table">
                                                                <thead>
                                                                    <tr>
                                                                        <th scolpe="col">Nome da empresa</th>
                                                                        <th scope="col">Nome do produto</th>
                                                                        <th scope="col">Preço pago na licitação</th>
                                                                        <th scope="col">Menor preço na internet</th>
                                                                        <th scope="col">Maior preço na internet</th>
                                                                    </tr>
                                                                </thead>
                                                                <tbody>
                                                                    <tr>
                                                                        <th scope="row">xxx</th>
                                                                        <td>xxx</td>
                                                                        <td>xxx</td>
                                                                        <td>xxx</td>
                                                                        <td>xxx</td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )}

                    </div>
                    <a className="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
                        <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span className="sr-only">Previous</span>
                    </a>
                    <a className="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
                        <span className="carousel-control-next-icon" aria-hidden="true"></span>
                        <span className="sr-only">Next</span>
                    </a>
                    {/* {empresas.map(empresa =>
                        <div className="modal fade" id={empresa.key.replace(/ /g, '')} tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div className="modal-dialog" role="document">
                                <div className="modal-content">
                                    <div className="modal-header">
                                        <h5 className="modal-title" id="exampleModalLabel">{empresa.key}</h5>
                                        <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div className="modal-body">
                            
                                    </div>
                                    <div className="modal-footer">
                                        <button type="button" className="btn btn-secondary" data-dismiss="modal">Close</button>
                                        <button type="button" className="btn btn-primary">Save changes</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )} */}
                </div>
                <hr />
            </section >


        );
    }
};
