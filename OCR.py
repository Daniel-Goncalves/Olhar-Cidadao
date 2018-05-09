import PyPDF2
import requests
from requests.auth import HTTPBasicAuth
import pycurl
from io import BytesIO
import base64
import json

def request_ocr(url,username,license_code, pdf_file):	

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


license_code = "3FFA295B-18E9-4954-B05F-7FE362D4D36E"
username =  "LUCASMOREIRA4887"

url = 'http://www.ocrwebservice.com/restservices/processDocument?gettext=true&language=brazilian&outputformat=xlsx&pagerange=5-6'

# Arquivo que será convertido
filePath = './x.pdf'

pdf_file = open(filePath,'rb')

response = request_ocr(url,username,license_code,pdf_file)

response = response.decode('UTF-8')
response_json = json.loads(response)
output_file_url = response_json['OutputFileUrl']

# Save xlsx
xlsx = requests.get(output_file_url)
with open('/home/daniel/Downloads/MYxlsx.xlsx', 'wb') as f:
    f.write(xlsx.content)


# Adapt this to one requisition for PDF page

# Extract tables from xlsx

# Save in the DB


