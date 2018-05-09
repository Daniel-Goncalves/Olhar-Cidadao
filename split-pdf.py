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

pdfs_to_be_split_list=[]

directory="./pdf"

for root,dirs,files in os.walk(directory):
    for filename in files:
        if filename.endswith('.pdf'):
            t=os.path.join(directory,filename)
            pdfs_to_be_split_list.append(t)
            ### APAGAR t


#Select one PDF file and create a lot of others PDF files into pdf folder
for i in range(0,len(pdfs_to_be_split_list)):

	filePath = pdfs_to_be_split_list[i]
	filename = filePath.split("/")[-1:][0][:-4]


	inputpdf = PdfFileReader(open(filePath, "rb"))
	for j in xrange(inputpdf.numPages):
		output = PdfFileWriter()
		output.addPage(inputpdf.getPage(j))
		with open("pdf/" + filename +str(j)  +".pdf", "wb") as outputStream:
			output.write(outputStream)
	