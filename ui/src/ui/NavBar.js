import React from 'react';
import { Link } from 'react-router'

const NavBar = (props) => {
  var pathName;
  var str = props.location.pathname;
  str = str.split("/");
  if (str[1] === 'graphs') pathName = true;
  else pathName = false;

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
      <div className="container">
        <Link to='/' className="navbar-brand js-scroll-trigger">Olhar Cidadão</Link>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive"
          aria-expanded="false" aria-label="Toggle navigation">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarResponsive">

          <ul className="navbar-nav ml-auto">
            {pathName ? (<li className="nav-ite">
              <a className="nav-link js-scroll-trigger text-white" href="#resume">Resumo</a>
            </li>) : (null)}
            {pathName ? (<li className="nav-ite">
              <a className="nav-link js-scroll-trigger text-white" href="#licitacoes">Licitações</a>
            </li>) : (null)}
            {pathName ? (<li className="nav-ite">
              <a className="nav-link js-scroll-trigger text-white" href="#comparation">Comparações</a>
            </li>) : (null)}
            <li className="nav-ite">
              <Link to='/api' className="nav-link js-scroll-trigger text-white">API</Link>
            </li>
            <li className="nav-ite">
              <a className="nav-link js-scroll-trigger text-white" href="#bout" data-toggle="modal" data-target="#about">Sobre</a>
            </li>
            <li className="nav-item">
              <a className="nav-link js-scroll-trigger text-white" href="#bout" data-toggle="modal" data-target="#contact">Contato</a>
            </li>
          </ul>


        </div>
      </div>
    </nav>
  );
};

export default NavBar;