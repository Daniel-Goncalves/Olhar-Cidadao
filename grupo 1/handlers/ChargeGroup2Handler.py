import base64
import logging
import tornado.web
from tornado import gen
import json
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import os
import xlrd


class ChargeGroup2Handler(tornado.web.RequestHandler):

	@gen.coroutine
	def create_column(df,nm):
		df['{}'.format(nm)]=[]

	@gen.coroutine
	# LEITURA DE ARQUIVO EXCEL RETORNANDO COMO DATAFRAME A ABA [0]
	def read_excel(file):
		return pd.ExcelFile(file).parse(pd.ExcelFile(file).sheet_names[0])
	
	@gen.coroutine
	def get():
		#CAMINHO (###Tem que alterar para o do docker que Grupo 1 ta usando!!###)
		path="../../Grupo2/Excel"


		#DATAFRAMES:
		df1 = pd.DataFrame({})
		tabela_unica = pd.DataFrame({})


		## SCRIPT


		#cria as colunas no dataframe1:
		create_column(df1,'Licitações')
		create_column(df1,'Lotes')


		#le a pasta path e obtem o nome das pastas das licitações como uma string
		arr_licitacoes=os.listdir(path)

		#lê cada pasta de licitações e obtem os lotes como strings
		arr_lotes=[]
		for diretorio in arr_licitacoes:
			arr_lotes+=[os.listdir('{}/{}'.format(path, diretorio))]


		### GRAVA NO DATAFRAME1 OS NOMES DE LICITAÇÕES E LOTES


		for i in range(len(arr_licitacoes)):
			if arr_licitacoes[i] in list(df1.Licitações):
				continue
			for k in range(len(arr_lotes[i])):
				df1 = df1.append({'Licitações':arr_licitacoes[i],'Lotes':arr_lotes[i][k]}, ignore_index=True)



		### CRIA AS COLUNAS NA TABELA_UNICA BASEADO NUME PRIMEIRA LEITURA DO PRIMEIRO LOTE

		lote = read_excel('{}/{}/{}'.format(path, df1.Licitações[0], df1.Lotes[0]))


		for nm in df1.columns:
			create_column(tabela_unica,nm)

		for nm in lote.columns:
			create_column(tabela_unica,nm)


		### ABRE CADA LOTE DO FORMATO EXCEL E COPIA AS LINHAS DO LOTE PARA A TABELA UNICA

		for i in range(len(df1)):
			if df1.Licitações[i] in list(tabela_unica.Licitações):
				continue
		lote = read_excel('{}/{}/{}'.format(path, df1.Licitações[i], df1.Lotes[i]))
		for k in range(len(lote)):
				tabela_unica = tabela_unica.append({'_id': ObjectId(), 'pdf_url': null, 'classificacao';: null, 'fiscal': null, 'valor_total': null, 'numero_processo':df1.Licitações[i],'edital':df1.Lotes[i], 'objeto':lote.Mercadoria[k], 'contrato': null, 'materiais_e_servicos': null, 'demandante': null, 'empresas': ['valor_estimado': null, 'nome_empresa': null, 'termo_aditivo': null, 'vigencia': null, 'valor_global': null, 'ata': null, 'descricao_empresa': null]'},ignore_index=True)

		records = json.loads(self.tabela_unica.T.to_json()).values()
		self.collection.insert(records)

		print(tabela_unica)
