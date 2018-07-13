import React from 'react'

const ModalAbout = (props) => {
  return (
    <div className="modal fade" id="about" tabIndex="-1" role="dialog" aria-labelledby="modalabout" aria-hidden="true">
      <div className="modal-dialog" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title" id="modalabout">Sobre</h5>
            <button type="button" className="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div className="modal-body">
            O projeto "Olhar Cidadão" visa disponibilizar aos cidadãos uma aplicação WEB para facilitar o acesso a dados dos portais de
transparência de órgãos públicos previamente definidos, especialmente em relação às compras e
contratações de serviços realizadas por estes órgãos públicos, a fim de potencializar a fiscalização popular.
              </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" data-dismiss="modal">Fechar</button>
          </div>
        </div>
      </div>
    </div>
  );
};
export default ModalAbout;