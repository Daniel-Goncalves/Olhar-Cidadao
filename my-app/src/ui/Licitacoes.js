import React, { Component } from 'react'

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
            materiais_suspects: [],
        };
    }
    componentDidMount() {
        let array = [];
        let aux = [];
        fetch("http://172.16.20.20/get_suspected_materials")
            .then(result => {
                return result.json();
            })
            .then(result => {
                console.log(result);
                let resultado = result['Materiais Suspeitos'];
                resultado.map(material => {
                    let control = 0;
                    for (let index = 0; index < aux.length; index++)
                        if (aux[index] === material.numero_processo)
                            control++;
                    if (control === 0)
                        aux.push(material.numero_processo);
                });
                let temp = [];
                let temp1 = [];

                for (let i = 0; i < aux.length; i++) {
                    temp1 = [];
                    let control = aux[i];
                    resultado.map((material, index) => {
                        if (material.numero_processo === control) {
                            temp1[index] = [material.suspect_company, material.suspected_product, material.price_in_bidding, material.suspect_company, material.more_expensive_found_product.origin, material.more_expensive_found_product.product, material.more_expensive_found_product.price];
                            temp[material.numero_processo.replace(/ /g, '').replace('/', '').replace(',', '').replace('.', '').replace('-', '')] = temp1;
                        }
                    });

                }
                this.setState({ materiais_suspects: temp });
                console.log(temp);
            });


        fetch("http://172.16.20.20/get_winner_companies")
            .then(result => {
                return result.json();
            })
            .then(result => {
                this.setState({ suspects: result['Winner companies'] });
            });

        let cont = 0;
        fetch('http://172.16.20.20/get_instituicao', {
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
                licitacoes.map(licitacao => {
                    array[cont] = licitacao.numero_processo;
                    cont++;
                })
                console.log(licitacoes);
                this.setState({
                    processos: array,
                    licitacoes: licitacoes
                })
                let aux = this.state.licitacoes;
                let temp = aux[0].fiscal;
                let element = document.getElementById(temp.replace(/ /g, ''));
                element.classList.add("active");
            });
    }


    render() {
        const processos = this.state.processos;
        const licitacoes = this.state.licitacoes;
        const empresas = this.state.suspects;
        const comparacoes = this.state.materiais_suspects;


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
                    <div style={{ textAlign: "center", width: "100%", padding: "20px" }}>
                        <div className="dropdown">
                            <button className="btn btn-secondary dropdown-toggle" style={{ width: '250px' }} type="button" id="botao_lic" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Escolha sua Licitação!</button>
                            <div className="dropdown-menu" id='div_lics' aria-labelledby="dropdownMenuButton">
                                {processos.map((i, index) => <li className="btn btn-light" data-target="#carousel_lic" data-slide-to={index} style={{ cursor: "pointer", marginLeft: "30px", marginBottom: "10px" }}>{i}</li>)}
                            </div>
                        </div>
                    </div>
                </div>
                <div id="carousel_lic" className="carousel slide" data-interval="false" data-ride="carousel">
                    <ol className="carousel-indicators">
                        {processos.map(index => <li data-target="#carousel_lic" data-slide-to={index}></li>)}
                    </ol>
                    <div className="carousel-inner">
                        {licitacoes.map(licitacao =>
                            <div id={licitacao.fiscal.replace(/ /g, '')} className="carousel-item">
                                <button type="button" className="btn btn-link" data-toggle="modal" data-target={"#" + licitacao.numero_processo.replace(/ /g, '').replace('/', '').replace('.', '')}><h3 className="col-3">{licitacao.numero_processo}</h3></button>
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
                                                <td><button type="button" className="btn btn-link" data-toggle="modal" data-target={"#" + empresa.nome_empresa.replace(/ /g, '').replace(',', '').slice(1, 6)}>{empresa.nome_empresa}</button></td>
                                                <td>R$ {parseFloat(empresa.valor_global.slice(2)).toLocaleString()} </td>
                                                <td>R$ {parseFloat(empresa.valor_estimado.slice(2)).toLocaleString()}</td>
                                                <td>{empresa.ata}</td>
                                                <td>{empresa.vigencia}</td>
                                            </tr>)}
                                    </tbody>
                                </table>
                                <div className='textAlign'>
                                    <button className="btn btn-danger marginBottom" type="button" data-toggle="collapse" data-target={"#COMP" + licitacao.numero_processo.replace(/ /g, '').replace('/', '').replace(',', '').replace('.', '').replace('-', '')} aria-expanded="false" aria-controls="collapseExample">Comparações</button>
                                    <p />
                                    <div className="collapse" id={"COMP" + licitacao.numero_processo.replace(/ /g, '').replace('/', '').replace(',', '').replace('.', '').replace('-', '')}>
                                        {(() => {
                                            let ok = comparacoes[licitacao.numero_processo.replace(/ /g, '').replace('/', '').replace(',', '').replace('.', '').replace('-', '')];
                                            console.log(ok);
                                            if (ok !== undefined) {
                                                return <div className="card card-body marginBottom">
                                                    <div className="accordion">
                                                        {ok.map((material, index) =>
                                                            <div className="card">
                                                                <div className="card-header" id="headingOne">
                                                                    <h5 className="mb-0">
                                                                        <button className="btn btn-link" type="button" data-toggle="collapse" data-target={"#" + index + material[0].replace(/ /g, '').slice(3, 10)} aria-expanded="true" aria-controls="collapseOne">
                                                                            {material[1].slice(0, 150)}
                                                                        </button>
                                                                    </h5>
                                                                </div>
                                                                <div id={index + material[0].replace(/ /g, '').slice(3, 10)} className="collapse" aria-labelledby="headingOne">
                                                                    <div className="card-body">
                                                                        <table className="table">
                                                                            <thead>
                                                                                <tr>
                                                                                    <th scolpe="col">Nome da empresa</th>
                                                                                    <th scope="col">Nome do produto pesquisado</th>
                                                                                    <th scope="col">Preço pago na licitação </th>
                                                                                    <th scope="col">Maior preço na internet </th>
                                                                                </tr>
                                                                            </thead>
                                                                            <tbody>
                                                                                <tr>
                                                                                    <th scope="row">{material[0]}</th>
                                                                                    <td>{material[5]}</td>
                                                                                    <td>R$ {material[2].toLocaleString()},00</td>
                                                                                    <td>R$ {material[6].toLocaleString()}</td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </div>
                                                                </div>

                                                            </div>
                                                        )}
                                                    </div>
                                                </div>;
                                            }
                                            else
                                                return <div>Essa licitação não possui nenhuma comparação!</div>

                                        })()}

                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
                <a className="carousel-control-prev" style={{ visibility: "hidden" }} href="#carouselExampleIndicators" role="button" data-slide="prev">
                    <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span className="sr-only">Previous</span>
                </a>
                <a className="carousel-control-next" style={{ visibility: "hidden" }} href="#carouselExampleIndicators" role="button" data-slide="next">
                    <span className="carousel-control-next-icon" aria-hidden="true"></span>
                    <span className="sr-only">Next</span>
                </a>
                {
                    empresas.map(empresa =>
                        <div className="modal fade" id={empresa.nome_empresa.replace(/ /g, '').replace(',', '').slice(1, 6)} tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div className="modal-dialog" role="document">
                                <div className="modal-content">
                                    <div className="modal-header">
                                        <h5 className="modal-title" id="exampleModalLabel">{empresa.nome_empresa}</h5>
                                        <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div className="modal-body">
                                        <div>
                                            Licitações ganhas: {empresa.number_of_wins}
                                        </div>
                                        <div>
                                            Valor total ganho: R$ {empresa.total_value.toLocaleString()}
                                        </div>

                                    </div>
                                    <div className="modal-footer">
                                        <button type="button" className="btn btn-secondary" data-dismiss="modal">Fechar</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )
                }
                {
                    licitacoes.map(licitacao =>
                        <div className="modal fade" id={licitacao.numero_processo.replace(/ /g, '').replace('/', '').replace('.', '')} tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div className="modal-dialog" role="document">
                                <div className="modal-content">
                                    <div className="modal-header">
                                        <h5 className="modal-title" id="exampleModalLabel">{licitacao.numero_processo}</h5>
                                        <button type="button" className="close" data-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div className="modal-body">
                                        <div>
                                            Edital: {licitacao.edital}
                                        </div>
                                        <div>
                                            Fiscal: {licitacao.fiscal}
                                        </div>
                                        <div>
                                            Valor total: R$ {parseFloat(licitacao.valor_total.slice(2)).toLocaleString()}
                                        </div>

                                    </div>
                                    <div className="modal-footer">
                                        <button type="button" className="btn btn-secondary" data-dismiss="modal">Fechar</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )
                }
                < hr />
            </section >


        );
    }
};
