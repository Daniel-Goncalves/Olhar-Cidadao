import React, { Component } from 'react'

var LineChart = require("react-chartjs").Line;
var contador = 0;
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
            datafull: [''],
            labelsfull: [''],
        };
    }
    componentDidMount() {
        fetch('http://172.16.20.20:8080/get_current_periods', {
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
                let arr = Object.values(result);
                let datafull = [''];
                let labelsfull = [''];
                arr.map(j => {
                    j.map((i, index) => {
                        datafull[index] = i.value;
                        labelsfull[index] = i.date;
                    })
                });
                let d = new Date();
                let n = d.getMonth();
                let data = [];
                let labels = [];
                let control = 0;
                let control2 = 0;
                for (let k = 0; k < 6; k++) {
                    if (parseInt(labelsfull[control].slice(5, 7)) === n) {
                        data[k] = datafull[control];
                        labels[k] = labelsfull[control];
                        control++;
                    }
                    else {
                        data[k] = 0;
                        let aux = n;
                        if (n < 10)
                            aux = '0' + n;
                        labels[k] = (parseInt(d.getFullYear()) - control2) + '-' + aux;
                    }
                    n--;
                    if (n === 0) {
                        n = 12;
                        control2++;
                    }
                }
                data.reverse();
                labels.reverse();
                this.setState({
                    datafull,
                    labelsfull,
                    data,
                    labels,
                });
            });
        fetch('http://172.16.20.20:8080/get_instituicao', {
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
                contador = 0;
                let licitacoes = result['Licitacoes dessa Instituicao'];
                licitacoes.map(licitacao => {
                    contador++;
                });

            });
    }
    teste(aux) {
        let option = aux.target.value;
        let d = new Date();
        let n = d.getMonth();
        let data = [];
        let labels = [];
        let control = 0;
        let control2 = 0;
        for (let k = 0; k < option; k++) {
            if (this.state.labelsfull[control] !== undefined)
                if (parseInt(this.state.labelsfull[control].slice(5, 7)) === n) {
                    data[k] = this.state.datafull[control];
                    labels[k] = this.state.labelsfull[control];
                    control++;
                }
                else {
                    data[k] = 0;
                    let aux = n;
                    if (n < 10)
                        aux = '0' + n;
                    labels[k] = (parseInt(d.getFullYear()) - control2) + '-' + aux;
                }
            else {
                data[k] = 0;
                let aux = n;
                if (n < 10)
                    aux = '0' + n;
                labels[k] = (parseInt(d.getFullYear()) - control2) + '-' + aux;
            }
            n--;
            if (n === 0) {
                n = 12;
                control2++;
            }
        }
        data.reverse();
        labels.reverse();
        this.setState({
            data,
            labels,
        });
    }
    render() {
        var str = window.location.href;
        str = str.split("/");
        var checkInt = false;
        if (str[5] === 'UnB')
            checkInt = true;

        const aux = this.state.labelsfull;
        return (
            <div>
                <section id="resume">
                    <div style={{ paddingLeft: "30px", paddingBottom: "60px" }}>
                        <div className="row">
                            <h2 style={{ paddingBottom: "30px" }} className="display-4 col-2">Resumo</h2><br />
                        </div>
                        <div className="row">
                            <div className="col-6">
                                <h3>Valor gasto com Licitações
                                    <button value='6' onClick={this.teste.bind(this)} style={{ marginLeft: "74px" }} className="btn btn-dark">6 meses</button>
                                    <button value='12' onClick={this.teste.bind(this)} style={{ marginLeft: "6px" }} className="btn btn-dark">1 ano</button>
                                    <button value='24' onClick={this.teste.bind(this)} style={{ marginLeft: "6px" }} className="btn btn-dark">2 anos</button>
                                </h3>
                                <LineChart data={returnGraf(this.state.labels, this.state.data)} width="675" height="350" />
                            </div>
                            <div className="col-5 text-center" style={{ marginTop: "20px", paddingLeft: "20px" }}>
                                <div className="container" style={{ marginLeft: "0px" }} >
                                    <h1 className="display-4">Pontuação</h1>
                                    <p className="lead">Aqui você pode conferir o nivel confiabilidade da empresa baseado em nossos algoritmos.</p>
                                </div>
                                <div className="progress" style={{ marginTop: "60px" }}>
                                    {checkInt ? (
                                        <div className="progress-bar" id="progress-bar1" role="progressbar" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100" style={{ width: "75%", backgroundColor: "#ffd900" }}></div>
                                    ) : (
                                            <div className="progress-bar" id="progress-bar1" role="progressbar" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100" style={{ width: "100%", backgroundColor: "green" }}></div>
                                        )}
                                </div>

                                <div style={{ paddingTop: "20px" }} className="row" id="div_info">
                                    <div className="col" id="info" style={{ borderRightStyle: "solid", borderWidth: "0.5px", borderColor: "grey" }}>
                                        <h5>{contador}</h5>
                                        <h6>Licitações Processadas</h6>
                                    </div>
                                    <div className="col" id="info">
                                        <h5>{checkInt ? '2' : '0'}</h5>
                                        <h6>licitacoes suspeitas</h6>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <hr />
                </section>
            </div >
        );
    }
}
