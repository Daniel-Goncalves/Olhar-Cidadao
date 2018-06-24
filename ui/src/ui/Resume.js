import React, { Component } from 'react'

var LineChart = require("react-chartjs").Line;

var data = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [{
        label: "My First dataset",
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: [0, 10, 5, 2, 20, 30, 45],
    }]
}

export default class Resume extends Component {
    constructor() {
        super();
        var str = window.location.href;
        str = str.split("/");
        this.state = {
            id: '',
            instituicao: str[5],
            data: ''
        };
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
                this.setState({ data: result });
            });
    }

    
    render() {

        var temp = this.state.data;
        console.log(temp);
        
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
                            <LineChart className="col-6" data={data} width="600" height="350" />
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