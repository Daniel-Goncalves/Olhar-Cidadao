import os

from os import chdir, getcwd, listdir, path

import pyPdf

from time import strftime


def check_path(prompt):

    abs_path = raw_input(prompt)

    while path.exists(abs_path) != True:

        print("\nThe specified path does not exist.\n")

        abs_path = raw_input(prompt)

    return abs_path   

 
directory="./"  
content = ""
name = "texto"

t=os.path.join(directory,'0document.pdf')
'''
print t

# Load PDF into pyPDF
path = t

pdf = pyPdf.PdfFileReader(file(path, "rb"))

# Iterate pages

for i in range(0, pdf.getNumPages()):

    # Extract text from page and add to content
    print("I:",i)
    print(pdf.getPage(i).extractText())
    content += pdf.getPage(i).extractText() + "\n"

print(content)
print(strftime("%H:%M:%S"), " pdf  -> txt ") 

f=open(name,'w')

f.write(content.encode("UTF-8"))

f.close
'''



lista=[]


for root,dirs,files in os.walk(directory):

    for filename in files:

        if filename.endswith('.pdf'):

            t=os.path.join(directory,filename)
            lista.append(t)




i=0
print lista

while i<=len(lista):

    path=lista[i]
    print path

    head,tail=os.path.split(path)   

    tail=tail.replace(".pdf",".txt")

    name=head+"/"+tail

    content = ""

    # Load PDF into pyPDF

    pdf = pyPdf.PdfFileReader(file(path, "rb"))

    # Iterate pages

    for i in range(0, pdf.getNumPages()):

        # Extract text from page and add to content

        content += pdf.getPage(i).extractText() + "\n"

    print(strftime("%H:%M:%S"), " pdf  -> txt ") 

    print content

    f=open(name,'w')

    f.write(content.encode("UTF-8"))

    f.close
