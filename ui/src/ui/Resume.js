import React from 'react'
import { Doughnut } from 'react-chartjs-2';


const Resume = (props) => {

    return (
        <section>
            <div>
                <Doughnut labels={"Red", "Blue", "Yellow", "Green", "Purple", "Orange"} data={[12, 19, 3, 5, 2, 3]} width={100} height={50} options={{ maintainAspectRatio: false }} />
            </div>
            <hr />
        </section>
    );
};
export default Resume;