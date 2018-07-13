import tornado.web
from tornado import gen
import logging
import sys
import json

from handlers.ConfigHandler import ConfigHandler
from handlers.CorsHandler import CorsHandler


class MaterialsSuspectedHandler(CorsHandler):

		
	@gen.coroutine
	def get(self):

		cursor = self.application.mongodb.suspected_materials.find()
		materials = yield MaterialsSuspectedHandler.get_materials(cursor)

		response = {
			'status': 'ok',
			'Materiais Suspeitos': materials,
		}
		self.set_status(200)  # http 200 ok
		self.write(response)
		self.finish()
		return


	@gen.coroutine
	def get_materials(cursor):
		material = {}
		array = []
		while (yield cursor.fetch_next):

			element = cursor.next_object()
			material = element
			del material["_id"]
			array.append(material)
			#print(array)

		return array

	@gen.coroutine
	def post(self):

		post_data = tornado.escape.json_decode(self.request.body)
		numero_processo = post_data['numero_processo']

		cursor = self.application.mongodb.suspected_materials.find({"numero_processo":numero_processo})
		materials = yield MaterialsSuspectedHandler.get_materials(cursor)

		if len(materials) == 0:
			# São retiradas as / do numero_processo para salvar o arquivo 
			# Logo, qnd vão para a colection os que possuem barra a perdem
			# Tratando caso específico de licitações com /
			if len(numero_processo) == 20:
				numero_processo = numero_processo[:12] + numero_processo[13:]

			cursor = self.application.mongodb.suspected_materials.find({"numero_processo":numero_processo})
			materials = yield MaterialsSuspectedHandler.get_materials(cursor)

		response = {
			'status': 'ok',
			'Materiais Suspeitos': materials,
		}
		self.set_status(200)  # http 200 ok
		self.write(response)
		self.finish()
		return
