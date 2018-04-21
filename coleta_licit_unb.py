#coding: latin1
from pymongo import MongoClient
import json
import BeautifulSoup
import pandas as pd
import requests
import re


# CHANGE COLLECTION ADDRESS
client = MongoClient('localhost', 27017)
db = client.projeto2
licit_collection = db.licitacoes

url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRjWfASCqM7XO-Frzf-DKIwOQF_cSd_LMKCh-DsgmDFAM2jPzxvbgFQbxHT9odmIfBhFsDzShhqlXtT/pubhtml'
# Get html code to match pdf urls after create dataframe
html = requests.get(url).content
soup = BeautifulSoup.BeautifulSoup(html)
table = soup.find("table")
html_table = BeautifulSoup.BeautifulSoup(str(table))

# Regex works, but too many urls apparently without a logic sequence...
#match = re.findall(r'href=[\'"]?([^\'" >]+)', table)
#if match:
	#print match[10]


def find_pdf_url(identifier):
	global html_table
	for tr in html_table.findAll("tr"):
		trs = tr.findAll("td")
		if len(trs) > 0:
			if len(trs) > 1 and trs[2].text == identifier:
				try:
					return trs[2].a["href"]
				except:		# Row does not have a pdf url
					return

table = pd.read_html(url)[0]
#columns = table.iloc[2].tolist() 	# This row actually represents the columns. Pop 0 because the first element is the row number
#columns.pop(0)
columns = ['objeto','numero_processo','materiais_e_servicos','contrato','empresas','edital','demandante','fiscal','valor_total','classificacao','pdf_url']

licit_df = pd.DataFrame(columns=columns)

objeto=numero_processo=materiais_e_servicos=ata=nome_empresa=edital=vigencia=valor_global=valor_estimado=demandante=fiscal=contrato=inicio_proxima_classificacao= None
licit_df_index = 0
empresas = []
new_object = True

def treat_table_row(row_info,state):
	global objeto,numero_processo,materiais_e_servicos,ata,nome_empresa,edital,vigencia,valor_global,valor_estimado,demandante,fiscal,licit_df_index,empresas,new_object,contrato,inicio_proxima_classificacao

	if table.iloc[index_row].notnull().sum() == 1:
		# Linha em branco -> Fim de ATAS COM VIGÊNCIA EXPIRADA
		inicio_proxima_classificacao = index_row + 3
		return False
	elif new_object:

		objeto = row_info[0]
		numero_processo = row_info[1]
		if state == "ATAS COM VIGÊNCIA EXPIRADA":
			materiais_e_servicos = row_info[2]
			ata = row_info[3]
			contrato = None
			termo_aditivo = None
		elif state == "CONTRATOS EXPIRADOS":
			materiais_e_servicos = None
			ata = None
			contrato = row_info[2]
			termo_aditivo = row_info[3]

		nome_empresa = row_info[4]
		edital = row_info[5]
		vigencia = row_info[6]
		valor_global = row_info[7]
		valor_estimado = row_info[8]
		demandante = row_info[9]
		fiscal = row_info[10]
		empresas.append({"ata":ata,"termo_aditivo":termo_aditivo,"nome_empresa":nome_empresa,"vigencia":vigencia,"valor_global":valor_global,"valor_estimado":valor_estimado})

		new_object = False
	elif table.iloc[index_row].notnull().sum() == 6:		# Outra empresa no mesmo objeto

		if state == "ATAS COM VIGÊNCIA EXPIRADA":
			ata = row_info[0]
			termo_aditivo = None
		elif state == "CONTRATOS EXPIRADOS":
			ata = None
			termo_aditivo = row_info[0]

		nome_empresa = row_info[1]
		vigencia = row_info[2]
		valor_global = row_info[3]
		valor_estimado = row_info[4]
		empresas.append({"ata":ata,"termo_aditivo":termo_aditivo,"nome_empresa":nome_empresa,"vigencia":vigencia,"valor_global":valor_global,"valor_estimado":valor_estimado})

	elif row_info[0] == "Valor Total:":	
		# Concluido um objeto
		valor_total = row_info[1]
		licit_df.loc[licit_df_index] = [objeto,numero_processo,materiais_e_servicos,contrato,empresas,edital,demandante,fiscal,valor_total,state,None]
		licit_df_index = licit_df_index + 1
		new_object = True
		empresas = []	
	return True


state = "ATAS COM VIGÊNCIA EXPIRADA"
for index_row in range(3,len(table)):
	row_info = table.iloc[index_row].tolist()
	row_info.pop(0)
	if(not treat_table_row(row_info,state)):
		break
	

empresas = []
new_object = True
state = "CONTRATOS EXPIRADOS"
for index_row in range(inicio_proxima_classificacao,len(table)):
	row_info = table.iloc[index_row].tolist()

	row_info.pop(0)
	if(not treat_table_row(row_info,state)):
		break


# Assign pdf urls
for i,(index, row) in enumerate(licit_df.iterrows()):

	if getattr(row, "classificacao") == "ATAS COM VIGÊNCIA EXPIRADA":
		identifier = getattr(row, "materiais_e_servicos")
	if getattr(row, "classificacao") == "CONTRATOS EXPIRADOS":
		identifier = getattr(row, "contrato")

	pdf_url = find_pdf_url(identifier)
	licit_df.loc[index]['pdf_url'] = pdf_url



#records = licit_df.to_json(orient='records')
records = json.loads(licit_df.T.to_json()).values()

# The correct would be use an update with upsert, but how it's a unique use script and all is inserted at once, 
# I stupdly just clear the collection
licit_collection.delete_many({})
licit_collection.insert(records)




#print table[0].iloc[8].isnull().sum()
#print table.iloc[0].notnull().sum()

