import React from 'react'


const Licitacoes = (props) => {
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
                            <li className="btn btn-light" data-target="#carousel_lic" data-slide-to="0" style={{ cursor: "pointer" }}>licitacao 1</li>
                            <li className="btn btn-light" data-target="#carousel_lic" data-slide-to="1" style={{ cursor: "pointer" }}>licitacao 2</li>
                            <li className="btn btn-light" data-target="#carousel_lic" data-slide-to="2" style={{ cursor: "pointer" }}>licitacao 3</li>
                        </div>
                    </div>
                </div>
            </div>
            <div id="carousel_lic" className="carousel slide" data-interval="false" data-ride="carousel">
                <ol className="carousel-indicators">
                    <li data-target="#carousel_lic" data-slide-to="0" className="active"></li>
                    <li data-target="#carousel_lic" data-slide-to="1"></li>
                    <li data-target="#carousel_lic" data-slide-to="2"></li>
                </ol>
                <div className="carousel-inner">
                    <div className="carousel-item active">
                        <h2 className="col-2">Licitacao 1</h2>

                        <table className="table">
                            <thead>
                                <tr>
                                    <th scope="col">Empresa</th>
                                    <th scope="col">Valor global</th>
                                    <th scope="col">Valor estimado</th>
                                    <th scope="col">Termo adtivo</th>
                                    <th scope="col">ata</th>
                                    <th scope="col">vigencia</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <th>xxx
                                        <image src="icons8-info-24.png" data-toggle="modal" data-target="#exampl" />
                                    </th>
                                    <td>xxx </td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                </tr>
                                <tr>
                                    <th scope="row">xxx <image src="icons8-info-24.png" data-toggle="modal" data-target="#exampleModal"></image></th>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                </tr>
                                <tr>
                                    <th scope="row">xxx <image src="icons8-info-24.png" data-toggle="modal" data-target="#exampleModal"></image></th>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                </tr>
                            </tbody>

                        </table>
                        <div style={{textAlign: "center"}} >
                            <button type="button" className="btn btn-danger btn-sm col-1" style={{marginBottom: "35px"}}>Comparações</button>
                        </div>
                    </div>
                    <div className="carousel-item">
                        <h2 className="col-2">Licitacao 2</h2>
                        <table className="table">
                            <thead>
                                <tr>
                                    <th scope="col">Empresa</th>
                                    <th scope="col">Valor global</th>
                                    <th scope="col">Valor estimado</th>
                                    <th scope="col">Termo adtivo</th>
                                    <th scope="col">ata</th>
                                    <th scope="col">vigencia</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <th scope="row">xxx <image src="icons8-info-24.png" data-toggle="modal" data-target="#exampleModal"></image></th>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                </tr>
                                <tr>
                                    <th scope="row">xxx <image src="icons8-info-24.png" data-toggle="modal" data-target="#exampleModal"></image></th>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                </tr>
                                <tr>
                                    <th scope="row">xxx <image src="icons8-info-24.png" data-toggle="modal" data-target="#exampleModal"></image></th>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                </tr>
                            </tbody>
                        </table>
                        <div style={{textAlign: "center"}} >
                            <button type="button" className="btn btn-danger btn-sm col-1" style={{marginBottom: "35px"}}>Comparações</button>
                        </div>
                    </div>
                    <div className="carousel-item">
                    <h2 className="col-2">Licitacao 3</h2>
                        <table className="table">
                            <thead>
                                <tr>
                                    <th scope="col">Empresa</th>
                                    <th scope="col">Valor global</th>
                                    <th scope="col">Valor estimado</th>
                                    <th scope="col">Termo adtivo</th>
                                    <th scope="col">ata</th>
                                    <th scope="col">vigencia</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <th scope="row">xxx <image src="icons8-info-24.png" data-toggle="modal" data-target="#exampleModal"></image></th>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                </tr>
                                <tr>
                                    <th scope="row">xxx <image src="icons8-info-24.png" data-toggle="modal" data-target="#exampleModal"></image></th>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                </tr>
                                <tr>
                                    <th scope="row">xxx <image src="icons8-info-24.png" data-toggle="modal" data-target="#exampleModal"></image></th>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                    <td>xxxx</td>
                                    <td>xxx</td>
                                </tr>
                            </tbody>
                        </table>
                        <div style={{textAlign: "center"}}>
                            <button type="button" className="btn btn-danger btn-sm col-1" style={{marginBottom: "35px"}}>Comparações</button>
                        </div>
                    </div>
                </div>
                <a className="carousel-control-prev" href="#carouselExampleIndicators" role="button" data-slide="prev">
                    <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                    <span className="sr-only">Previous</span>
                </a>
                <a className="carousel-control-next" href="#carouselExampleIndicators" role="button" data-slide="next">
                    <span className="carousel-control-next-icon" aria-hidden="true"></span>
                    <span className="sr-only">Next</span>
                </a>
            </div>
            <hr />
        </section>


    );
};
export default Licitacoes;