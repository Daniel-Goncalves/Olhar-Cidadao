import tornado.web
from tornado import gen
import logging
import sys
import json

from handlers.ConfigHandler import ConfigHandler
from handlers.CorsHandler import CorsHandler


class ProcessosHandler(CorsHandler):

		
	@gen.coroutine
	def post(self):

		post_data = tornado.escape.json_decode(self.request.body)

		entry = post_data['nome_empresa']

		cursor = self.application.mongodb.licitacoes.find()
		numero_processo = yield ProcessosHandler.get_numero_processo(cursor,entry)

		response = {
			'status': 'ok',
			'Numero do processo' : numero_processo,
		}
		self.set_status(200)  # http 200 ok
		self.write(response)
		self.finish()
		return


	@gen.coroutine
	def get_numero_processo(cursor,entry):
		numero_processo = {}
		array = []
		#entry = "LDC Bortolozzi – Comercial - ME"

		while (yield cursor.fetch_next):
			
			element = cursor.next_object()
			numero_processo = element["numero_processo"]
			empresas = element["empresas"]
			for empresa in empresas:
				nome = empresa["nome_empresa"]
				if(entry == nome):
					array.append(numero_processo)

		return array