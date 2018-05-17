import PyPDF2
import requests
import pycurl
from io import BytesIO
import base64
import json
import os, sys
from os import chdir, getcwd, listdir, path
import traceback
import pandas as pd

from handlers.ConfigHandler import ConfigHandler


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

def get_all_xlss_files():
	#Get all .pdf files of the path
	tables_to_be_treated=[]

	directory="./pdf"

	for root,dirs,files in os.walk(directory):
		for filename in files:
			if filename.endswith('.xlsx'):
				t=os.path.join(directory,filename)
				tables_to_be_treated.append(t)
	
	return tables_to_be_treated


def split_one_pdf(filePath):
	
	filename = filePath.split("/")[-1:][0][:-4]

	splited_pdf_files_names = []

	inputpdf = PyPDF2.PdfFileReader(open(filePath, "rb"))
	for j in range(inputpdf.numPages):
		output = PyPDF2.PdfFileWriter()
		output.addPage(inputpdf.getPage(j))

		new_file_path = "pdf/" + filename +str(j)  +".pdf"
		splited_pdf_files_names.append(new_file_path)

		with open(new_file_path, "wb") as outputStream:
			output.write(outputStream)

	return splited_pdf_files_names




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

def extract_data_from_xlsx(filename,first_page):

	dfs = pd.read_excel(filename, sheet_name="Sheet1")

	# Delete rows with at least 2 null values
	dfs = dfs.dropna(thresh=2)

	objects = []
	for i,(index, row) in enumerate(dfs.iterrows()):  # go through all rows
		if not (first_page and i == 0):		# If not columns names
			json = {"item":row[0],"quantidade":row[1],"unidade":row[2],"especificacoes":row[3],"valor_unitario":row[4],"fornecedor":row[5]}
			objects.append(json)
	return objects

def push_list_elements_in_another(list1,list2):
	for element in list1:
		list2.append(element)

def delete_all_extensions_files(dir_name,extension):
	all_files = os.listdir(dir_name)
	for item in all_files:
	    if item.endswith("." + extension):
	        os.remove(os.path.join(dir_name, item))

def extract_objects_from_xlsx_files_and_insert_in_db(self):

		delete_all_extensions_files("./pdf","pdf")

		xlsx_files_names = get_all_xlss_files()
		all_table_objects = []
		new_objects = []
		for i,(table) in enumerate(xlsx_files_names):
			
			if i is 0:	# It's the first page of the original PDF, só the first line will correspond to the columns names
				new_objects = extract_data_from_xlsx(table,True)
			else:
				new_objects = extract_data_from_xlsx(table,False)

			push_list_elements_in_another(new_objects,all_table_objects)

		# Save in the DB
		materials_collection = self.application.mongodb.materials
		all_table_objects.forEach((item) => materials_collection.insert(item))

		delete_all_extensions_files("./pdf","xlsx")


def get_licenses_array():
	licenses_array = []


	return licenses_array


def prepare_pdfs_and_send_requests(self):
	# PDFs to be treated
	pdfs_to_be_split_list = get_all_pdfs_files()

	# Treate each one PDF
	for i in range(0,len(pdfs_to_be_split_list)):
		filePath = pdfs_to_be_split_list[i]

		# Separate the n pages of a pdf in n pdfs
		# That's because the ocr requisition can only treat one pdf page at a time
		splited_pdf_files_names = split_one_pdf(filePath)

		# Make one requisition for each pdf then treat the xlsx outputs in order to get the table

		# PUXAR ARRAY DE LICENSES

		position_in_license_array = 0
		licenses_array = get_licenses_array()
		username = licenses_array[position_in_license_array]['username']
		license_code =  licenses_array[position_in_license_array]['license_code']


		# Go through all the pdfs to be converted to xlsx
		for j in range(0,len(splited_pdf_files_names)):

			filePath = splited_pdf_files_names[j]
			pdf_file = open(filePath,'rb')


			allowed_to_proceed = False

			while not allowed_to_proceed:

				print("Converting pdf to xlsx:",pdf_file)
				response = request_ocr(username,license_code,pdf_file)
				response_json = json.loads(response.decode('UTF-8'))
				output_file_url = response_json['OutputFileUrl']
				response_error = response_json['ErrorMessage']

				if response_error:
					print("Error while making ocr request:",response_error)
					if str(response_error) == "Daily page limit exceeded":
						print("Page Limit exceeded. Switching key")
						if position_in_license_array == len(licenses_array) - 1:
							print("No more keys")
							delete_all_extensions_files("./pdf","pdf")
							delete_all_extensions_files("./pdf","xlsx")
							return
						else:
							position_in_license_array = position_in_license_array + 1
							username = licenses_array[position_in_license_array]['username']
							license_code = licenses_array[position_in_license_array]['license_code']
				else:
					allowed_to_proceed = True

					print("Downloading xlsx from:",output_file_url,"\n")

					# Save xlsx
					xlsx = requests.get(output_file_url)
					with open(filePath[:-4] + '.xlsx', 'wb') as f:
						f.write(xlsx.content)
				print("Unexpected error while converting to xlsx:", traceback.format_exc())

		extract_objects_from_xlsx_files_and_insert_in_db(self)



prepare_pdfs_and_send_requests()