import tornado.web
from tornado import gen
import logging
import sys
import json

from handlers.ConfigHandler import ConfigHandler


class MaterialsSuspectedHandler(tornado.web.RequestHandler):

		
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
			print(array)

		return array
