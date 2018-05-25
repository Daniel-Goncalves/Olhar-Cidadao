import tornado.web
from tornado import gen
import logging
import sys

from handlers.ConfigHandler import ConfigHandler


class CompaniesHandler(tornado.web.RequestHandler):

		
	@gen.coroutine
	def get(self):

		cursor = self.application.mongodb.licitacoes.find({"classificacao":"ATAS COM VIGÊNCIA EXPIRADA"})
		winner_companies = yield CompaniesHandler.get_winner_companies(cursor)

		response = {
			'status': 'ok',
			'Winner companies': winner_companies,
		}
		self.set_status(200)  # http 200 ok
		self.write(response)
		self.finish()
		return


	@gen.coroutine
	def get_winner_companies(cursor):
		winner_companies = {}
		
		while (yield cursor.fetch_next):

			element = cursor.next_object()
			companies = element['empresas']

			for company in companies:
				# Company has already won any process
				if company['nome_empresa'] in winner_companies:
					winner_companies[company['nome_empresa']] += 1
				else:
					winner_companies[company['nome_empresa']] = 1

		return winner_companies