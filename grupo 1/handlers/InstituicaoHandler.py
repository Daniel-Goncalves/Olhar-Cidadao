import tornado.web
from tornado import gen
import logging
import sys
import json

from handlers.CorsHandler import CorsHandler
from handlers.ConfigHandler import ConfigHandler


class InstituicaoHandler(CorsHandler):

		
	@gen.coroutine
	def get(self):
		cursor =  yield self.application.mongodb.licitacoes.distinct("instituicao")

		response = {"instituicoes":cursor}
		self.set_status(200)  # http 200 ok
		self.write(response)
		self.finish()
		return 