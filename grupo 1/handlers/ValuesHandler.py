import tornado.web
from tornado import gen
import logging
import sys

from handlers.ConfigHandler import ConfigHandler
from handlers.CorsHandler import CorsHandler


class ValuesHandler(CorsHandler):

		
	@gen.coroutine
	def get(self):


		cursor = self.application.mongodb.licitacoes.find({"classificacao":"ATAS COM VIGÊNCIA EXPIRADA"})

		all_results_list = yield ValuesHandler.compare_total_values(self,cursor)

		response = {
			'status': 'ok',
			'Total values analyze': all_results_list
		}
		self.set_status(200)  # http 200 ok
		self.write(response)
		self.finish()
		return


	@gen.coroutine
	def compare_total_values(self,cursor):


		all_results_list = []
		while (yield cursor.fetch_next):

			element = cursor.next_object()
			objeto = element['objeto']
			valor_total = element['valor_total']

			print(objeto)
			
			#print(valor_total,"\n")

			#result = self.application.mongodb.materials.aggregate([{"$group": {"filename": objeto, "valor_total_materiais": {"$sum": "$valor_unitario"}}}])

			result = self.application.mongodb.materials.aggregate([
				{"$match": {"filename":objeto}},
				{"$project":{
					"valor_unitario":1,
					"quantidade":1,
					"especificacoes":1
			  	}}
			])

			# Go through all matched documents
			expected_total_value = 0
			while (yield result.fetch_next):

				element = result.next_object()
				valor_unitario = element['valor_unitario']
				qtd = element['quantidade']
				
				# OCR does not convert all numbers right. For example in PDF SERVIÇO DE INTALAÇÃO DE FORROS all the quantities like 1.000,2.000,4.000... are converted as 1,2,4...
				#qtd = str(qtd).replace(".","")

				try:
					qtd = int(qtd)

					if objeto == "SERVIÇO DE INTALAÇÃO DE FORROS":
						qtd = qtd * 1000

				except ValueError:
					qtd = 1

				# Convert unitary value
				new_valor_unitario = ""
				valor_unitario = valor_unitario.replace("\n","")

				if objeto == "FORNECIMENTO DE REFLETORES LED":
					print("Initial value:",valor_unitario)

				for index,letra in enumerate(valor_unitario):

					try:
						number = int(letra)
					except ValueError:

						if letra == ",":
							number = "."
						else:
							number = ""

					new_valor_unitario = new_valor_unitario + str(number)

				# Exceptions treatment
				# If it does not end with a number
				while not new_valor_unitario[-1].isdigit():
					new_valor_unitario = new_valor_unitario[0:-1]
				# If it has more than one point
				if(len(new_valor_unitario.split(".")) > 2):
					new_valor_unitario = ""
					for index,value in enumerate(new_valor_unitario):
						new_valor_unitario += value
						if index == 0:
							new_valor_unitario += "."
				
				# If cannot convert valor_unitario to number(wrong format...) do not treat it
				# If value is above some limiar, it's probably wrong so ignore it...
				try:
					new_valor_unitario = float(new_valor_unitario)

					if new_valor_unitario < ConfigHandler.maximum_unit_value:

						material_price = new_valor_unitario * int(qtd)
						expected_total_value += material_price

						if objeto == "FORNECIMENTO DE REFLETORES LED":
							print("Qtd:",qtd)
							print("Unit:",new_valor_unitario)
							print(material_price)
				except ValueError:
					#print("Doing nothing","Value:",new_valor_unitario,"qtd:",qtd)
					do_nothing = True

			all_results_list.append({"File":objeto,"Expected aproximated total value":expected_total_value,"Real total value":valor_total})
			#print("File:",objeto)
			#print("Expected total value:",expected_total_value)
			#print("Real total value:",valor_total)
		
		return all_results_list