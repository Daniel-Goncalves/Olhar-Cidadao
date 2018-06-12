#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
from tornado import gen
import sys, os, json, time, re
import logging
from handlers.InitScrapy import InitScrapy

from handlers.ConfigHandler import ConfigHandler


class SuspectedMaterialsHandler(tornado.web.RequestHandler):

	@gen.coroutine
	def post(self):
		# Deleta o arquivo de resultados já obtidos:
		if os.path.isfile('results.json'):
			os.remove("results.json")

		# Respond before...
		self.set_status(200)  # http 200 ok
		self.write("Analyzing products prices...")
		self.finish()

		# Conexão com o banco de dados e início do processo de validação de dados:
		SuspectedMaterialsHandler.import_from_db(self)
		
	@gen.coroutine
	def import_from_db(self):

		# Importação dos dados dos materiais das licitações:
		cursor = self.application.mongodb.materials.find({"especificacoes":"VIDRO LAMINADO INCOLOR E = 10 mm\nAPLICACAÇÃO: portas, janelas e\niluminação zenital. CARACTERÍSTICA(S):\nplanos, lisos, transparentes, com superfícies"})

		# Para cada material do BD:
		while (yield cursor.fetch_next):
			material = cursor.next_object()
			# Se a unidade não for 'Hora' (o que significa que é um serviço, fora do escopo do projeto):

			print("Running spider for material: ",material['especificacoes'][:40])

			if material['unidade'] != 'Hora':
				# Este produto será validado:
				yield SuspectedMaterialsHandler.validate_product(self,material)

	@gen.coroutine
	def validate_product(self, product):
		# A descrição do produto, o preço unitário e o nome do fornecedor são extraídos:

		product_name = product['especificacoes']
		suspect_price = product['valor_unitario']
		suspect_company = product['fornecedor']

		# O objeto da classe Scrapy é criado com os dados do produto. Será considerado um máximo de 40 caracteres.
		# A função get_data() buscará preços na internet e retornará o resultado no arquivo results.json:

		if product_name != None:#"Pé Conico Cromado 15cm":

			InitScrapy.get_data(product_name[:40])

			# Listas de resultados e de preços:
			results = []
			prices = []

			# Criação de flag para indicar corrupção:
			flag_corruption = False
			
			# Tratamento do preço do produto para float:
			suspect_price_temp = re.sub("[^0-9,]", "", suspect_price)
			suspect_price_float = float(suspect_price_temp.replace(',','.'))

			# O arquivo results.json é aberto e cada linha é um dicionário.
			# Popula-se a lista de preços já convertidos em float.
			# Popula-se a lista de resultados com vários dicionários:

			
			with open('results.json') as file:
				for line in file.readlines():
					data = json.loads(line)
					price_temp = re.sub("[^0-9,]", "", data['price'])
					price_float = float(price_temp.replace(',','.'))
					prices.append(price_float)
					results.append(data)

			# Deleta o arquivo de resultados já obtidos:
			os.remove("results.json")

			# Se o valor máximo da lista de preços for menor que o preço na licitação, é uma suspeita de corrupção:
			if max(prices) < suspect_price_float:
				price = max(prices)
				index = prices.index(max(prices)) 
				flag_corruption = True

			# Se a flag de corrupção estiver setada como verdadeira:
			if flag_corruption:
				# Um dicionário com a data atual e os dados do produto suspeito são armazenados num dicionário:
				suspect_data = { "more_expensive_found_product":{"price":results[index]['price'],"origin":results[index]['origin'],"store":results[index]['store'],"product":results[index]['product']},"date" : time.strftime("%x"), "suspected_product" : product_name,"price_in_bidding":suspect_price_float , "suspect_company" : suspect_company }

				# O dicionário criado acima será mesclado com cada dicionário da lista de resultados:
				for result in results:
					result.update(suspect_data)

				print("CORRUPÇÃO!")

				# Os dados serão inseridos numa nova collection do BD:
				# Conexão com o BD é feita:
				self.application.mongodb.suspected_materials.insert(suspect_data)