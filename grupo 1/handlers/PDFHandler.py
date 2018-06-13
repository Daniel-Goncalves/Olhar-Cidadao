import tornado.web
from tornado import gen
import logging
import sys
import requests
import base64
import json
from urllib.request import urlopen
import PyPDF2
from io import BytesIO
import os
from os import chdir, getcwd, listdir, path
import traceback
import pandas as pd
import pycurl


from handlers.ConfigHandler import ConfigHandler


class PDFHandler(tornado.web.RequestHandler):

	@gen.coroutine
	def download_pdf(redirect_link,file_name):
		logging.debug("Downloading PDF: {0}".format(file_name))
		file_name = "./pdf/" + file_name + ".pdf"
		if redirect_link:

			redirect_page = str( urlopen(redirect_link).read() )
 
			# Get real link from redirect page
			#pdf_link = redirect_page.split("href=")[1][1:].split(">")[0][:-1]
			pdf_link = redirect_page.split("url=")[1].split(">")[0][:-1]

			with open(file_name, "wb") as file:
				# get request
				response = requests.get(pdf_link)		

				#logging.debug(response.content)		# As code
				# write to file
				file.write(response.content)	# As file

				# Now send to the handler that extracts unitary value from pdf, add it to the document and save in the DB

	@gen.coroutine
	def download_all_pdfs(self):

		# Somente ATAS COM VIGÊNCIA EXPIRADA possuem relações de materiais
		# Portanto, puxar somente objetos dessa classe ( contrato é nulo)

		cursor =  self.application.mongodb.licitacoes.find({"classificacao":"ATAS COM VIGÊNCIA EXPIRADA"})

		while (yield cursor.fetch_next):
			element = cursor.next_object()
			url = element['pdf_url']
			filename = element['objeto']
			PDFHandler.download_pdf(url,filename)

	@gen.coroutine
	def get_all_pdfs_files():
	#Get all .pdf files of the path
		pdfs_to_be_split_list=[]

		directory="./pdf"

		for root,dirs,files in os.walk(directory):
			for filename in files:
				if filename.endswith('.pdf'):
					t=os.path.join(directory,filename)
					pdfs_to_be_split_list.append(t)
		
		return pdfs_to_be_split_list

	@gen.coroutine
	def get_all_xls_files():
		#Get all .pdf files of the path
		tables_to_be_treated=[]

		directory="./pdf"

		for root,dirs,files in os.walk(directory):
			for filename in files:
				if filename.endswith('.xlsx'):
					t=os.path.join(directory,filename)
					tables_to_be_treated.append(t)
		
		return tables_to_be_treated

	@gen.coroutine
	def delete_file_if_exists(filePath):
		try:
			os.remove(filePath)
		except OSError:
			pass

	@gen.coroutine
	def split_one_pdf(filePath,filename):
		
		filename = filePath.split("/")[-1:][0][:-4]

		splited_pdf_files_names = []

		inputpdf = PyPDF2.PdfFileReader(open(filePath, "rb"),strict=False)
		for j in range(inputpdf.numPages):
			output = PyPDF2.PdfFileWriter()
			output.addPage(inputpdf.getPage(j))

			new_file_path = "./pdf/" + filename +str(j)  +".pdf"
			splited_pdf_files_names.append(new_file_path)

			# Delete if exists
			yield PDFHandler.delete_file_if_exists(new_file_path)
			
			with open(new_file_path, "wb") as outputStream:
				output.write(outputStream)

		return splited_pdf_files_names

	@gen.coroutine
	def request_ocr(username,license_code, pdf_file):	

		url = ConfigHandler.ocrwebserviceURL

		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(pycurl.URL, url)
		c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
		c.setopt(c.USERPWD,username + ":" + license_code)
		c.setopt(c.CUSTOMREQUEST, "POST")
		c.setopt(c.POST, True)

		c.setopt(pycurl.PUT, 1)
		c.setopt(c.READDATA, pdf_file)
		c.setopt(c.WRITEDATA, buffer)
		#c.setopt(c.INFILESIZE, len(pdf_file))

		c.perform()
		c.close()

		body = buffer.getvalue()
		return body

	@gen.coroutine
	def find_table_columns_names(row,column):

		if column == "item":
			columns_names_array = ConfigHandler.item_names_array
		if column == "quantidade":
			columns_names_array = ConfigHandler.qtd_names_array
		if column == "unidade":
			columns_names_array = ConfigHandler.und_names_array
		if column == "especificacoes":
			columns_names_array = ConfigHandler.especificacoes_names_array
		if column == "valor_unitario":
			columns_names_array = ConfigHandler.valor_unit_names_array
		if column == "fornecedor":	
			columns_names_array = ConfigHandler.fornecedor_names_array



		position = 0
		for field in row:
			if(field.lower() in columns_names_array):
				return position
			position +=1


	@gen.coroutine
	def extract_data_from_xlsx(table,filename,first_page,indexes_list):

		dfs = pd.read_excel(table, sheet_name="Sheet1")

		# Delete rows with at least 2 null values
		dfs = dfs.dropna(thresh=2)

		objects = []

		for i,(index, row) in enumerate(dfs.iterrows()):  # go through all rows
			if not (first_page and i == 0):		# If not columns names

				json = {"item":row[indexes_list[0]],"quantidade":row[indexes_list[1]],"unidade":row[indexes_list[2]],"especificacoes":row[indexes_list[3]],"valor_unitario":row[indexes_list[4]],"fornecedor":row[indexes_list[5]],"filename":filename}
				objects.append(json)
		return objects

	@gen.coroutine
	def get_columns_indexes(table):
		dfs = pd.read_excel(table, sheet_name="Sheet1")

		# Delete rows with at least 2 null values
		dfs = dfs.dropna(thresh=2)

		for i,(index, row) in enumerate(dfs.iterrows()):  # go through all rows
			## Get from the first line then return
			item_index = yield PDFHandler.find_table_columns_names(row,"item")
			unidade_index = yield PDFHandler.find_table_columns_names(row,"unidade")
			quantidade_index = yield PDFHandler.find_table_columns_names(row,"quantidade")
			especificacoes_index = yield PDFHandler.find_table_columns_names(row,"especificacoes")
			valor_unitario_index = yield PDFHandler.find_table_columns_names(row,"valor_unitario")
			fornecedor_index = yield PDFHandler.find_table_columns_names(row,"fornecedor")

			indexes_list = [item_index,quantidade_index,unidade_index,especificacoes_index,valor_unitario_index,fornecedor_index]

			#print("Index List:",indexes_list)
			return indexes_list

	@gen.coroutine
	def push_list_elements_in_another(list1,list2):
		for element in list1:
			list2.append(element)

	@gen.coroutine
	def delete_all_extensions_files(dir_name,extension):
		all_files = os.listdir(dir_name)
		for item in all_files:
			if item.endswith("." + extension):
				os.remove(os.path.join(dir_name, item))

	@gen.coroutine
	def extract_objects_from_xlsx_files_and_insert_in_db(self,original_filename,delete_xlsx):

			xlsx_files_names = yield PDFHandler.get_all_xls_files()

			first_page = 'pdf/' + original_filename + "0.xlsx"
			indexes_list = yield PDFHandler.get_columns_indexes(first_page)
			all_table_objects = []
			new_objects = []
			for i,(table) in enumerate(xlsx_files_names):
				
				if i is 0 and first_page != original_filename:	# It's the first page of the original PDF, só the first line will correspond to the columns names
					new_objects = yield PDFHandler.extract_data_from_xlsx(table,original_filename,True, indexes_list)
				else:
					new_objects = yield PDFHandler.extract_data_from_xlsx(table,original_filename,False , indexes_list)

				yield PDFHandler.push_list_elements_in_another(new_objects,all_table_objects)

			# Save in the DB
			materials_collection = self.application.mongodb.materials
			logging.debug("Inserting materials in DB: {0}".format(all_table_objects))


			#materials_collection.insert(all_table_objects)
			for record in all_table_objects:
				materials_collection.update({'especificacoes':record['especificacoes'],'filename':record['filename'],'item':record['item']},record,upsert=True)
			
			# Command to delete duplicated materials
			# db.materials.find({},{especificacoes:1,filename:1,item:1}).sort({_id:1}).forEach(function(doc){db.materials.remove({_id:{$gt:doc._id},especificacoes:doc.especificacoes,filename:doc.filename,item:doc.item})})


			if delete_xlsx:
				yield PDFHandler.delete_all_extensions_files("./pdf","xlsx")
		
	@gen.coroutine
	def get_licenses_array(self):

		cursor = self.application.mongodb.licenses.find()
		licenses_array = yield cursor.to_list(length=180)
		return licenses_array

	@gen.coroutine
	def prepare_pdfs_and_send_requests(self):
		# PDFs to be treated
		logging.debug("Preparing to make OLC requests...")
		pdfs_to_be_split_list = yield PDFHandler.get_all_pdfs_files()

		# Get Licenses
		position_in_license_array = 0
		licenses_array = yield PDFHandler.get_licenses_array(self)

		username = licenses_array[position_in_license_array]['username']
		license_code =  licenses_array[position_in_license_array]['license_code']

		logging.debug("Username: {0}".format(username))

		# Treate each one PDF
		logging.debug("Treating each PDF...")

		for i in range(0,len(pdfs_to_be_split_list)):
			treated_pdf_file_path = pdfs_to_be_split_list[i]
			filename = treated_pdf_file_path.split("/")[-1:][0][:-4]

			# Separate the n pages of a pdf in n pdfs
			# That's because the ocr requisition can only treat one pdf page at a time
			splited_pdf_files_names = yield PDFHandler.split_one_pdf(treated_pdf_file_path,filename)

			# Make one requisition for each pdf then treat the xlsx outputs in order to get the table
			
			# Go through all the pdfs to be converted to xlsx
			for j in range(0,len(splited_pdf_files_names)):

				allowed_to_proceed = False
				while not allowed_to_proceed:

					filePath = splited_pdf_files_names[j]
					pdf_file = open(filePath,'rb')

					logging.debug("Converting pdf to xlsx: {0}".format(pdf_file))
					response = yield PDFHandler.request_ocr(username,license_code,pdf_file)
					response_json = json.loads(response.decode('UTF-8'))
					output_file_url = response_json['OutputFileUrl']
					response_error = response_json['ErrorMessage']

					if response_error:

						logging.debug("Error while making ocr request: {0}".format(response_error))
						if str(response_error) == "Daily page limit exceeded":
							logging.debug("Page Limit exceeded for " + username + ". Switching key")
							key_switched = True
							if position_in_license_array == len(licenses_array) - 1:
								logging.debug("No more keys")
								PDFHandler.delete_all_extensions_files("./pdf","pdf")
								PDFHandler.delete_all_extensions_files("./pdf","xlsx")
								return
							else:
								position_in_license_array = position_in_license_array + 1
								username = licenses_array[position_in_license_array]['username']
								license_code = licenses_array[position_in_license_array]['license_code']
								logging.debug("New user name: {0}".format(username))
					else:
						allowed_to_proceed = True
						logging.debug("Downloading xlsx from:{0}\n".format(output_file_url))

						# Save xlsx
						xlsx = requests.get(output_file_url)
						with open(filePath[:-4] + '.xlsx', 'wb') as f:
							f.write(xlsx.content)

			

			yield PDFHandler.extract_objects_from_xlsx_files_and_insert_in_db(self,filename,True)

			#Delete treated PDFs
			for pdf in splited_pdf_files_names:
				os.remove(pdf)
			os.remove(treated_pdf_file_path)

		logging.debug("Removing all PDFs files")
		logging.debug("Materials Charge Successfully Executed!")
		PDFHandler.delete_all_extensions_files("./pdf","pdf")
