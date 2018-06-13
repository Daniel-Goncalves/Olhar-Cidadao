import tornado.web
from tornado import gen
import logging
import sys
import json

from handlers.ConfigHandler import ConfigHandler


class EmpresasHandler(tornado.web.RequestHandler):

		
	@gen.coroutine
	def get(self):

		cursor = self.application.mongodb.licitacoes.find()
		empresas = yield EmpresasHandler.get_empresas(cursor)

		response = {
			'status': 'ok',
			'Empresas': empresas,
		}
		self.set_status(200)  # http 200 ok
		self.write(response)
		self.finish()
		return


	@gen.coroutine
	def get_empresas(cursor):
		empresas = {}
		array = []
		
		while (yield cursor.fetch_next):
			
			element = cursor.next_object()
			empresas = element["empresas"]
			array.append(empresas)

		return array