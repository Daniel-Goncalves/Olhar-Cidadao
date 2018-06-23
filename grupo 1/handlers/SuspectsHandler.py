import tornado.web
from tornado import gen
import logging


from handlers.ConfigHandler import ConfigHandler
from handlers.CorsHandler import CorsHandler


class SuspectsHandler(CorsHandler):


	@gen.coroutine
	def get(self):

		cursor = self.application.mongodb.suspicious_biddings.find({})
		suspects_array = []
		while (yield cursor.fetch_next):
			element = cursor.next_object()
			del element['_id']
			suspects_array.append(element)

		response = {"suspecious":suspects_array}

		self.set_status(200)
		self.write(response)
		self.finish()
		return