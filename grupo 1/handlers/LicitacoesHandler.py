import tornado.web
from tornado import gen
import logging
import sys
import json

from handlers.ConfigHandler import ConfigHandler


class LicitacoesHandler(tornado.web.RequestHandler):

		
	@gen.coroutine
	def get(self):

		cursor = self.application.mongodb.licitacoes.find()
		licitacoes = yield LicitacoesHandler.get_licitacao(cursor)

		response = {
			'status': 'ok',
			'licitacoes': licitacoes,
		}
		self.set_status(200)  # http 200 ok
		self.write(response)
		self.finish()
		return


	@gen.coroutine
	def get_licitacao(cursor):
		licitacao = {}
		array = []
		
		while (yield cursor.fetch_next):

			element = cursor.next_object()
			licitacao = element
			del licitacao["_id"]
			array.append(licitacao)
			print(array)

		return array