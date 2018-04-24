import os

from os import chdir, getcwd, listdir, path

import pyPdf

from time import strftime


def check_path(prompt):

    abs_path = raw_input(prompt)

    while path.exists(abs_path) != True:

        print "\nThe specified path does not exist.\n"

        abs_path = raw_input(prompt)

    return abs_path   

   

print "\n"





list=[]

directory="tt"

for root,dirs,files in os.walk(directory):

    for filename in files:

        if filename.endswith('.pdf'):

            t=os.path.join(directory,filename)

            list.append(t)


m=len(list)

i=0

while i<=len(list):

    path=list[i]

    head,tail=os.path.split(path)

    var="\\"

   

    tail=tail.replace(".pdf",".txt")

    name=head+var+tail


    content = ""

    # Load PDF into pyPDF

    pdf = pyPdf.PdfFileReader(file(path, "rb"))

    # Iterate pages

    for i in range(0, pdf.getNumPages()):

        # Extract text from page and add to content

        content += pdf.getPage(i).extractText() + "\n"

    print strftime("%H:%M:%S"), " pdf  -> txt "

    f=open(name,'w')

    f.write(content.encode("UTF-8"))

    f.close
