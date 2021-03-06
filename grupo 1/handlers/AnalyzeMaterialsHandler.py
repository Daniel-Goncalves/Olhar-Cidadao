#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
from tornado import gen
import sys, os, json, time, re
import logging
from handlers.InitScrapy import InitScrapy

from handlers.ConfigHandler import ConfigHandler
from handlers.CorsHandler import CorsHandler


class AnalyzeMaterialsHandler(CorsHandler):

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
		AnalyzeMaterialsHandler.import_from_db(self)
		
	@gen.coroutine
	def import_from_db(self):

		# Importação dos dados dos materiais das licitações:
		cursor = self.application.mongodb.materials.find({},no_cursor_timeout=True)

		# Para cada material do BD:
		i = 1
		while (yield cursor.fetch_next):
			material = cursor.next_object()
			# Se a unidade não for 'Hora' (o que significa que é um serviço, fora do escopo do projeto):

			print(str(i) + ") Running spider for material: ",material['especificacoes'][:40])
			i+=1
			if material['unidade'] != 'Hora':
				# Este produto será validado:
				yield AnalyzeMaterialsHandler.validate_product(self,material)
		cursor.close()

	@gen.coroutine
	def validate_product(self, product):
		# A descrição do produto, o preço unitário e o nome do fornecedor são extraídos:

		product_name = product['especificacoes']
		suspect_price = product['valor_unitario']
		suspect_company = product['fornecedor']
		numero_processo = product['numero_processo']

		# O objeto da classe Scrapy é criado com os dados do produto. Será considerado um máximo de 40 caracteres.
		# A função get_data() buscará preços na internet e retornará o resultado no arquivo results.json:

		count = yield self.application.mongodb.already_searched_products.find({"material":product_name}).count()
		if product_name != None and count <= 0:#"Pé Conico Cromado 15cm":

			InitScrapy.get_data(product_name[:20])

			# Listas de resultados e de preços:
			results = []
			prices = []

			# Criação de flag para indicar corrupção:
			flag_corruption = False


			try:
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
						#print("price_temp:",price_temp)
						price_float = float(price_temp.replace(',','.'))
						#print("price_float:",price_float)

						prices.append(price_float)
						results.append(data)

				# Deleta o arquivo de resultados já obtidos:
				os.remove("results.json")

				# Se o valor máximo da lista de preços for menor que o preço na licitação, é uma suspeita de corrupção:
				if len(prices) != 0 and max(prices) < suspect_price_float and suspect_price_float < ConfigHandler.maximum_unit_value:
					price = max(prices)
					index = prices.index(max(prices)) 
					flag_corruption = True

				# Se a flag de corrupção estiver setada como verdadeira:
				if flag_corruption:
					# Um dicionário com a data atual e os dados do produto suspeito são armazenados num dicionário:
					suspect_data = { "more_expensive_found_product":{"price":results[index]['price'],"origin":results[index]['origin'],"store":results[index]['store'],"product":results[index]['product']},"date" : time.strftime("%x"), "suspected_product" : product_name,"price_in_bidding":suspect_price_float , "suspect_company" : suspect_company ,"numero_processo":numero_processo}

					# O dicionário criado acima será mesclado com cada dicionário da lista de resultados:
					for result in results:
						result.update(suspect_data)

					print("CORRUPÇÃO!")

					# Os dados serão inseridos numa nova collection do BD:
					# Conexão com o BD é feita:
					self.application.mongodb.suspected_materials.insert(suspect_data)
				self.application.mongodb.already_searched_products.insert({"material":product_name})
			except:
				self.application.mongodb.already_searched_products.insert({"material":product_name})
				print("Error in some point of material treatment...",sys.exc_info()[0])
