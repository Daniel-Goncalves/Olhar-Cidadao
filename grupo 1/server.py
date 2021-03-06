# Tornado Web Server
import tornado.ioloop
import tornado.web
import tornado.httpserver
import motor
import sys
import logging
import os
import time

from handlers.ConfigHandler import ConfigHandler
from handlers.ChargeUnbBiddingsHandler import ChargeUnbBiddings
from handlers.ValuesHandler import ValuesHandler
from handlers.CompareCompaniesHandler import CompareCompaniesHandler
from handlers.CompaniesHandler import CompaniesHandler
from handlers.ProcessosHandler import ProcessosHandler
from handlers.LicitacoesHandler import LicitacoesHandler
from handlers.SuspectedBiddingsHandler import SuspectedBiddingsHandler
from handlers.ChargeGroup2Handler import ChargeGroup2Handler
from handlers.InstituicoesHandler import InstituicoesHandler
from handlers.AnalyzeMaterialsHandler import AnalyzeMaterialsHandler
from handlers.MaterialsSuspectedHandler import MaterialsSuspectedHandler
from handlers.CurrentPeriodsHandler import CurrentPeriodsHandler

def create_web_server():

    # Diretorio onde sao salvos os conteudos estaticos
    static_path = os.path.join(os.path.dirname(__file__), "static")

    # Roteamento para as diferentes URIs
    handlers = [
        (r"/olhar_cidadao/charge_unb_biddings", ChargeUnbBiddings),
        (r"/olhar_cidadao/charge_grupo2", ChargeGroup2Handler),
        (r"/olhar_cidadao/get_values_differences", ValuesHandler),
        (r"/olhar_cidadao/get_winner_companies", CompareCompaniesHandler),
        (r"/olhar_cidadao/get_empresas", CompaniesHandler),
        (r"/olhar_cidadao/get_empresa", CompaniesHandler),
        (r"/olhar_cidadao/get_processos", ProcessosHandler),
        (r"/olhar_cidadao/get_licitacoes", LicitacoesHandler),
        (r"/olhar_cidadao/get_instituicao", InstituicoesHandler),
        (r"/olhar_cidadao/get_instituicoes",InstituicoesHandler),
        (r"/olhar_cidadao/get_suspects", SuspectedBiddingsHandler),
	    (r"/olhar_cidadao/get_suspected_materials", MaterialsSuspectedHandler),
        (r"/olhar_cidadao/search_suspected_materials",AnalyzeMaterialsHandler),
        (r"/olhar_cidadao/get_current_periods",CurrentPeriodsHandler),
        #(r"/(.*)", tornado.web.StaticFileHandler, {'path': static_path,
        #                                           "default_filename": "index.html"})
    ]

    return tornado.web.Application(handlers)


def __configure_logging():
    log_level = ConfigHandler.log_level
    numeric_level = getattr(logging, log_level.upper(), None)
    logging.basicConfig(level=numeric_level, filename=ConfigHandler.log_file)

if __name__ == '__main__':

    # Le a porta a ser usada a partir da configuracao lida
    http_listen_port = 8080

    web_app = create_web_server()
    ioloop = tornado.ioloop.IOLoop.instance()

    # Pool do Motor (MongoDB)
    mongo_dsn = 'localhost:27017' 

    web_app.mongodb = motor.motor_tornado.MotorClient(
        host=mongo_dsn,
        minPoolSize=ConfigHandler.mongodb_min_pool_size,
        connect=True,
        appname="LicitacoesWebServer"
    )[ConfigHandler.mongodb_db_name]

    __configure_logging()

    web_app.listen(http_listen_port)
    logging.debug(
        'Started application on port %d',
        int(http_listen_port))
    print('Started application on port', int(http_listen_port))

    ioloop.start()
