from pyPdf import PdfFileWriter, PdfFileReader
import os
from os import chdir, getcwd, listdir, path
import os, sys
import re

"""
#Just for an specific .pdf

inputpdf = PdfFileReader(open("pdf/teste.pdf", "rb"))

for i in xrange(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("pdf/document-page%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)

"""

#Get all .pdf files of the path

list=[]

directory="pdf"

for root,dirs,files in os.walk(directory):
    for filename in files:
        if filename.endswith('.pdf'):
            t=os.path.join(directory,filename)
            list.append(t)

m=len(list)
print(list[0])
i=0

#Select one PDF file and create a lot of others PDF files into a new path
for i in xrange(m):
	print(list[i])
	ofolder = list[i]
	nfolder = ofolder.replace(".", "")
	
	if not os.path.exists(nfolder):
		os.mkdir(nfolder)
	name = ofolder
	#print(name)
	#print(nfolder)
	inputpdf = PdfFileReader(open(name, "rb"))
	for j in xrange(inputpdf.numPages):
		output = PdfFileWriter()
		output.addPage(inputpdf.getPage(j))
		with open("%s/document-page%d.pdf" % (nfolder, j), "wb") as outputStream:
			output.write(outputStream)
