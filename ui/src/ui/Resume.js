import React, { Component } from 'react'

var LineChart = require("react-chartjs").Line;
var mes = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}
var precosTotais = {};
var ultimos = number => {
    return [
        number,
        number - 1,
        number - 2,
        number - 3,
        number - 4,
        number - 5,
    ];
}
var date = new Date().getMonth();
var returnGraf = (labels, dados) => ({
    labels: labels,
    datasets: [{
        label: "Valor gasto com licitações",
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: dados,
    }]
});

export default class Resume extends Component {
    constructor() {
        super();
        var str = window.location.href;
        str = str.split("/");
        this.state = {
            id: '',
            instituicao: str[5],
            data: [''],
            labels: [''],
        };
    }
    componentDidMount() {
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
                licitacoes.map(licitacao => {
                    let result = /\d{2}\/(\d{2})\/(\d{4}) - \d{2}\/\d{2}\/\d{4}/.exec(licitacao.empresas[0].vigencia);

                    let chave = result[2] + parseInt(result[1]);
                    if (precosTotais[chave]) {
                        precosTotais[chave] += parseFloat(licitacao.valor_total.slice(2));
                    } else {
                        precosTotais[chave] = parseFloat(licitacao.valor_total.slice(2));
                    }
                    return licitacao;
                });
                let labels = ultimos(date).map(asd => {
                    return (mes[asd + 1]);
                }).reverse();
                let data = ultimos(date).map(asd => {
                    return precosTotais["2018" + (asd + 1)] || 0;
                }).reverse();
                let teste = [0, 0, 0, 0, 0, 0];
                if (JSON.stringify(data) !== JSON.stringify(teste))
                    this.setState({
                        labels,
                        data,
                    });
                else
                    this.setState({
                        labels: labels,
                        data: teste,
                    });
            });
    }
    render() {
        return (
            <div>
                <section id="resume">
                    <div style={{ paddingLeft: "30px", paddingBottom: "60px" }}>
                        <div className="row">
                            <h2 style={{ paddingBottom: "30px" }} className="display-4 col-2">Resumo</h2><br />
                            <div className="col-7"></div>
                            <h2 style={{ paddingBottom: "30px", paddingRight: "10px", paddingTop: "20px" }} className="display-5 col-2">{this.state.instituicao}</h2><br />
                        </div>
                        <div className="row">
                            <LineChart className="col-6" data={returnGraf(this.state.labels, this.state.data)} width="675" height="350" />
                            <div className="col-5 text-center" style={{ marginTop: "20px", paddingLeft: "20px" }}>
                                <div className="container" style={{ marginLeft: "0px" }} >
                                    <h1 className="display-4">Pontuação</h1>
                                    <p className="lead">Aqui você pode conferir o nivel confiabilidade da empresa baseado em nossos algoritmos.</p>
                                </div>
                                <div className="progress" style={{ marginTop: "60px" }}>
                                    <div className="progress-bar" id="progress-bar1" role="progressbar" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100" style={{ width: "17%", }}></div>
                                </div>

                                <div style={{ paddingTop: "20px" }} className="row" id="div_info">
                                    <div className="col" id="info" style={{ borderRightStyle: "solid", borderWidth: "0.5px", borderColor: "grey" }}>
                                        <h5>221</h5>
                                        <h6>Licitações Concluidas</h6>
                                    </div>
                                    <div className="col" id="info" style={{ borderRightStyle: "solid", borderWidth: "0.5px", borderColor: "grey" }}>
                                        <h5>10</h5>
                                        <h6>Licitações Concluidas no ultimo ano</h6>
                                    </div>
                                    <div className="col" id="info">
                                        <h5>2</h5>
                                        <h6>licitacoes suspeitas</h6>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <hr />
                </section>
            </div>
        );
    }
}