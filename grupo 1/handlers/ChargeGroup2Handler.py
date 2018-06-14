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
		#CAMINHO 
		path="handlers/Excel"


		#DATAFRAMES:
		df_materiais = pd.DataFrame({})
		df_licitacoes = pd.DataFrame({})
		df_lotes = pd.DataFrame({})
		tabela_unica = pd.DataFrame({})

		## SCRIPT


		#cria as colunas nos dataframes:
		create_column(df_licitacoes,'Licitações')
		create_column(df_licitacoes,'Lotes')

		create_column(df_lotes,'Licitações')
		create_column(df_lotes,'Lotes')


		#le a pasta path e obtem o nome das pastas das licitações como uma string
		arr_licitacoes=os.listdir(path)

		#lê cada pasta de licitações e obtem os lotes como strings
		arr_lotes=[]
		arr_infos=[]
		for diretorio in arr_licitacoes:
			arr_lotes+=[os.listdir('{}/{}'.format(path, diretorio))]
			arr_infos+=[os.listdir('{}/{}/{}'.format(path, diretorio,'Lotes'))]
		arr_lotes2 = copy.deepcopy(arr_lotes)   

		for i in range(len(arr_lotes2)):
			for j in range(len(arr_lotes2[i])):
				if arr_lotes2[i][j] == 'Lotes':
					arr_lotes[i].remove(arr_lotes[i][j])
				else:
					continue 
		arr_lotes3 = copy.deepcopy(arr_lotes)

		for k in range(len(arr_lotes3)):
    			for l in range(len(arr_lotes3[k])):
        			if arr_lotes3[k][l][0] == '.':
            				arr_lotes[k].remove(arr_lotes[k][l])
            				break
        			else:
            				continue 
		### GRAVA NO DATAFRAME1 OS NOMES DE LICITAÇÕES E LOTES


		for i in range(len(arr_licitacoes)):
    			if arr_licitacoes[i] in list(df_licitacoes.Licitações):
        			continue
    			for k in range(len(arr_lotes[i])):
        			df_licitacoes = df_licitacoes.append({'Licitações':arr_licitacoes[i],'Infos':arr_lotes[i][k]}, ignore_index=True)
    
		for i in range(len(arr_licitacoes)):
    			if arr_licitacoes[i] in list(df_lotes.Licitações):
        			continue
    			for k in range(len(arr_infos[i])):
        			df_lotes = df_lotes.append({'Licitações':arr_licitacoes[i],'Lotes':arr_infos[i][k]}, ignore_index=True)
    
		### CRIA AS COLUNAS NA TABELA_UNICA BASEADO NUME PRIMEIRA LEITURA DO PRIMEIRO LOTE

		lote = read_excel('{}/{}/{}'.format(path, df_licitacoes.Licitações[0], df_licitacoes.Infos[0]))
		info = read_excel('{}/{}/{}/{}'.format(path, df_lotes.Licitações[0], 'Lotes', df_lotes.Lotes[0])) 

		create_column(tabela_unica,'pdf_url')
		create_column(tabela_unica,'classificacao')
		create_column(tabela_unica,'fiscal')
		create_column(tabela_unica,'valor_total')
		create_column(tabela_unica,'numero_processo')
		create_column(tabela_unica,'edital')
		create_column(tabela_unica,'objeto')
		create_column(tabela_unica,'contrato')
		create_column(tabela_unica,'materiais_e_servicos')
		create_column(tabela_unica,'demandante')
		create_column(tabela_unica,'empresas')

		create_column(df_materiais,'especificacoes')
		create_column(df_materiais,'quantidade')
		create_column(df_materiais,'valor_unitario')
		create_column(df_materiais,'item')
		create_column(df_materiais,'fornecedor')
		create_column(df_materiais,'unidade')
		create_column(df_materiais,'filename')
	

		### ABRE CADA LOTE DO FORMATO EXCEL E COPIA AS LINHAS DO LOTE PARA A TABELA UNICA
		
		for i in range(len(df_licitacoes)):
			if df_licitacoes.Licitações[i] in list(tabela_unica.numero_processo):
				continue
			lote = read_excel('{}/{}/{}'.format(path, df_licitacoes.Licitações[i], df_licitacoes.Infos[i]))
			info = read_excel('{}/{}/{}/{}'.format(path, df_lotes.Licitações[i], 'Lotes', df_lotes.Lotes[i])) 
			for k in range(len(lote)):
				tabela_unica = tabela_unica.append({'pdf_url': None, 'classificacao': 'ATAS COM VIGÊNCIA EXPIRADA', 'fiscal': lote.pregoeiro[k], 'valor_total': 'R$ {}'.format(lote.ValorArrematado[k]), 'numero_processo':df_licitacoes.Licitações[i],'edital':lote.edital[k], 'objeto':lote.Descricao[k], 'contrato': None, 'materiais_e_servicos': 'SRP 632/2016', 'demandante': 'DISER', 'empresas': [{'valor_estimado': 'R$ {}'.format(lote.ValorUnitário[k]), 'nome_empresa': lote.Nome_Fantasia[k], 'termo_aditivo': None, 'vigencia': lote.vigencia[k], 'valor_global': 'R$ {}'.format(lote.ValorArrematado[k]), 'ata': None, 'descricao_empresa': lote.Atividade_Economica[k]}]},ignore_index=True)
			for j in range(len(info)):    
				df_materiais = df_materiais.append({'especificacoes': info.Descrição[j], 'quantidade': info.Quantidade[j], 'valor_unitario': lote.ValorUnitário[j], 'item': info.Item[j], 'fornecedor': lote.Nome_Fantasia[j], 'unidade': None, 'filename':None}, ignore_index=True)

		records = json.loads(self.tabela_unica.T.to_json()).values()
		self.licitacoes.insert(records)
		
		records2 = json.loads(self.df_materiais.T.to_json()).values()
		self.materiais.insert(records2)
		print(tabela_unica)
