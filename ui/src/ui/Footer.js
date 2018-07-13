import React from 'react'

const Footer = (props) => {
    var pathName;
    var str = props.location.pathname;
    str = str.split("/");
    if (str[1] === 'graphs') pathName = true;
    else pathName = false;

    return (
        pathName ?
            <footer id="footer" className="py-3 bg-dark">
                <div className="container">
                    <p className="m-0 text-center text-white">Copyright 2018 &copy; Universidade de Brasília | Faculdade de Tecnologia | Todos os direitos reservados.</p>
                </div>
            </footer>
            :
            <footer style={{ position: "absolute", bottom: "0", width: "100%", height: "60px" }} id="footer" className="py-3 bg-dark">
                <div className="container">
                    <p className="m-0 text-center text-white">Copyright 2018 &copy; Universidade de Brasília | Faculdade de Tecnologia | Todos os direitos reservados.</p>
                </div>
            </footer>
    );
};
export default Footer;