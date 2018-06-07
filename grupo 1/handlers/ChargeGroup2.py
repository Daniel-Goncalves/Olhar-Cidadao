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


class ChargeGrupo2(tornado.web.RequestHandler):

	@gen.coroutine
	def create_column(df,nm):
    		df[f'{nm}']=[]

	@gen.coroutine
	# LEITURA DE ARQUIVO EXCEL RETORNANDO COMO DATAFRAME A ABA [0]
	def read_excel(file):
		return pd.ExcelFile(file).parse(pd.ExcelFile(file).sheet_names[0])
	
	@gen.coroutine
	def generate_df():
		#CAMINHO (###Tem que alterar para o do docker que Grupo 1 ta usando!!###)
		path="//Excel"


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
			arr_lotes+=[os.listdir(f'{path}//{diretorio}')]


		### GRAVA NO DATAFRAME1 OS NOMES DE LICITAÇÕES E LOTES


		for i in range(len(arr_licitacoes)):
			if arr_licitacoes[i] in list(df1.Licitações):
				continue
			for k in range(len(arr_lotes[i])):
				df1 = df1.append({'Licitações':arr_licitacoes[i],'Lotes':arr_lotes[i][k]}, ignore_index=True)


		# SAIDA DO DATAFRAME 1 | CONTEM TODAS AS PASTAS E LOTES COMO UM INDICE QUE SERA USADO DEPOIS
		df1


		### CRIA AS COLUNAS NA TABELA_UNICA BASEADO NUME PRIMEIRA LEITURA DO PRIMEIRO LOTE

		lote = le_excel(f'{path}//{df1.Licitações[0]}//{df1.Lotes[0]}')


		for nm in df1.columns:
			create_column(tabela_unica,nm)

		for nm in lote.columns:
			create_column(tabela_unica,nm)


		### ABRE CADA LOTE DO FORMATO EXCEL E COPIA AS LINHAS DO LOTE PARA A TABELA UNICA

		for i in range(len(df1)):
			if df1.Licitações[i] in list(tabela_unica.Licitações):
				continue
		lote = le_excel(f'{path}//{df1.Licitações[i]}//{df1.Lotes[i]}')
		for k in range(len(lote)):
        		tabela_unica = tabela_unica.append({'Licitações':df1.Licitações[i],'Lotes':df1.Lotes[i],'Item':lote.Item[k],'Descrição':lote.Descrição[k],'Quantidade':lote.Quantidade[k],'Mercadoria':lote.Mercadoria[k]},ignore_index=True)


		
