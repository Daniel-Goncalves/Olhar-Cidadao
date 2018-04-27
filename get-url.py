import pymongo
import sys
import urllib2

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.projeto2
licit = db.licitacoes

url_array = []
i = 0
test = ""

cursor = licit.find({},{"pdf_url": True, "_id": False})
for pdf_url in cursor:
	url_array.append(pdf_url)
	response = urllib2.urlopen(url_array.append(pdf_url))
	file = open(i + "document.pdf", 'w')
	file.write(response.read())
	file.close()
	print("Completed")
	i = i + 1

