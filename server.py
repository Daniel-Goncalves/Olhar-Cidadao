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

def create_web_server():

    # Diretorio onde sao salvos os conteudos estaticos
    static_path = os.path.join(os.path.dirname(__file__), "static")

    # Roteamento para as diferentes URIs
    handlers = [
        (r"/charge_unb_biddings", ChargeUnbBiddings)
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
    http_listen_port = 9000

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
