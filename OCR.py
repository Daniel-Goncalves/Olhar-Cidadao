import PyPDF2
import requests
from requests.auth import HTTPBasicAuth
import pycurl
from io import BytesIO
import base64
import json
import os, sys
from os import chdir, getcwd, listdir, path
import traceback

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


def prepare_pdfs_and_send_requests():
	# PDFs to be treated
	pdfs_to_be_split_list = get_all_pdfs_files()

	# Treate one PDF
	for i in range(0,len(pdfs_to_be_split_list)):
		filePath = pdfs_to_be_split_list[i]

		# Separate the n pages of a pdf in n pdfs
		# That's because the ocr requisition can only treat one pdf page at a time
		splited_pdf_files_names = split_one_pdf(filePath)

		# Make one requisition for each pdf then treat the xlsx outputs in order to get the table

		license_code = "3FFA295B-18E9-4954-B05F-7FE362D4D36E"
		username =  "LUCASMOREIRA4887"

		# Go through all the pdfs to be converted to xlsx
		for j in range(0,len(splited_pdf_files_names)):

			filePath = splited_pdf_files_names[j]
			pdf_file = open(filePath,'rb')


			try:
				print("Converting pdf to xlsx:",pdf_file)

				response = request_ocr(username,license_code,pdf_file)
				response = response.decode('UTF-8')
				response_json = json.loads(response)
				output_file_url = response_json['OutputFileUrl']
				response_error = response_json['ErrorMessage']

				if response_error:
					print("Error while making ocr request:",response_error)
					return

				print("Downloading xlsx from:",output_file_url,"\n")

				# Save xlsx
				xlsx = requests.get(output_file_url)
				with open(filePath + '.xlsx', 'wb') as f:
					f.write(xlsx.content)

			except Exception as e:
				print("Unexpected error while converting to xlsx:", traceback.format_exc())


			
		# Delete all pdf files

		# Extract tables from xlsx

		# Save in the DB

		# Delete all xlsx files

prepare_pdfs_and_send_requests()