import tornado.web
from tornado import gen
import logging
import sys
import json

from handlers.CorsHandler import CorsHandler
from handlers.ConfigHandler import ConfigHandler


class InstituicoesHandler(CorsHandler):

	@gen.coroutine
	def get(self):

		cursor =  yield self.application.mongodb.licitacoes.distinct("instituicao")

		response = {"instituicoes":cursor}
		self.set_status(200)  # http 200 ok
		self.write(response)
		self.finish()
		return

	@gen.coroutine
	def post(self):

		post_data = tornado.escape.json_decode(self.request.body)

		entry = post_data['instituicao']

		cursor = self.application.mongodb.licitacoes.find()
		instituicao = yield InstituicoesHandler.get_instituicao(cursor,entry)

		response = {
			'status': 'ok',
			'Licitacoes dessa Instituicao' : instituicao,
		}
		self.set_status(200)  # http 200 ok
		self.write(response)
		self.finish()
		return


	@gen.coroutine
	def get_instituicao(cursor,entry):
		instituicao = {}
		licitacao = {}
		array = []
		#entry = "LDC Bortolozzi – Comercial - ME"
		#entry = "UnB"
		while (yield cursor.fetch_next):
			
			element = cursor.next_object()
			licitacao = element
			instituicao = element["instituicao"]
			if(entry == instituicao):
				del licitacao["_id"]
				array.append(licitacao)

		return array
