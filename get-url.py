import pymongo
import sys
import urllib2
from pymongo import MongoClient
import requests
import pyPdf
from StringIO import StringIO

def download_pdf(redirect_link):
	global i

	if redirect_link:

		redirect_page = urllib2.urlopen(redirect_link).read()

		# Get real link from redirect page
		pdf_link = redirect_page.split("href=")[1][1:].split(">")[0][:-1]
		pdf = urllib2.urlopen(pdf_link).read()

		return pdf
		#file = open(str(i) + "document.pdf", 'w')
		#file.write(pdf)
		#file.close()
		#i = i + 1



client = MongoClient('localhost', 27017)
db = client.projeto2
licit = db.licitacoes

url_array = []
i = 0

cursor = licit.find({},{"pdf_url": True, "_id": False})
for pdf_url in cursor:
	url_array.append(pdf_url)
	#download_pdf(pdf_url['pdf_url'])

pdf = download_pdf(url_array[0]['pdf_url'])
pdf = pyPdf.PdfFileReader(StringIO(pdf))


# Iterate pages
content = ""
for i in range(0, pdf.getNumPages()):

	# Extract text from page and add to content

	content += pdf.getPage(i).extractText() + "\n"

#print(strftime("%H:%M:%S"), " pdf  -> txt ") 

print(content)


#print(url_array)



