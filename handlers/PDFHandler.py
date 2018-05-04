import tornado.web
from tornado import gen
import sys
from urllib.request import urlopen
from pymongo import MongoClient
from requests import get
import PyPDF2
from io import StringIO


class PDFHandler(tornado.web.RequestHandler):

	@gen.coroutine
	def download_pdf(redirect_link,file_name):
		file_name = file_name + ".pdf"
		if redirect_link:

			redirect_page = str( urlopen(redirect_link).read() )
 
			# Get real link from redirect page
			#pdf_link = redirect_page.split("href=")[1][1:].split(">")[0][:-1]
			pdf_link = redirect_page.split("url=")[1].split(">")[0][:-1]

			with open(file_name, "wb") as file:
				# get request
				response = get(pdf_link)		

				#print(response.content)		# As code
				# write to file
				file.write(response.content)	# As file

				# Now send to the handler that extracts unitary value from pdf, add it to the document and save in the DB





'''
# Iterate pages
content = ""
for i in range(0, pdf.getNumPages()):

	# Extract text from page and add to content

	content += pdf.getPage(i).extractText() + "\n"

#print(strftime("%H:%M:%S"), " pdf  -> txt ") 

print(content)


#print(url_array)
'''