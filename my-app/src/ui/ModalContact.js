import React from 'react'

const ModalContact = (props) => {
  return (
    <div className="modal fade" id="contact" tabIndex="-1" role="dialog" aria-labelledby="modalabout" aria-hidden="true">
      <div className="modal-dialog" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title" id="modalabout">Contato</h5>
            <button type="button" className="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div className="modal-body">
            <b>Professor:</b>flavioelias@unb.br <br />
            <b>Gerente de Projeto:</b> lcsvncs429@gmail.com <br />
            <b>GitHub:</b> https://github.com/Daniel-Goncalves/Olhar-Cidadao <br />
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" data-dismiss="modal">Fechar</button>
          </div>
        </div>
      </div>
    </div>
  );
};
export default ModalContact;