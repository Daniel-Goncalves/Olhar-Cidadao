import React from 'react'


const Resume = (props) => {
    return (
        <section>
            <div className="container">
                <div className="row">
                    <div className="col-4 text-center">
                        <h3>Valor Gasto</h3>
                        <canvas style={{ height: "400px" }} id="myChart"></canvas>
                    </div>
                    <div className="col-4 text-center">
                        <h3>Distruibuição de Verba</h3>
                        <canvas id="pieChart"></canvas>
                    </div>
                </div>
            </div>
        </section>
    );
};
export default Resume;