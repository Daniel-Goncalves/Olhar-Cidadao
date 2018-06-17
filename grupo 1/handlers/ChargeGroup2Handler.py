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
import copy


class ChargeGroup2Handler(tornado.web.RequestHandler):

	@gen.coroutine
	def create_column(df,nm):
		df['{}'.format(nm)]=[]

	@gen.coroutine
	# LEITURA DE ARQUIVO EXCEL RETORNANDO COMO DATAFRAME A ABA [0]
	def read_excel(file):
		return pd.ExcelFile(file).parse(pd.ExcelFile(file).sheet_names[0])
	
	@gen.coroutine
	def get(self):
		#CAMINHO 
		path="handlers/Excel"


		#DATAFRAMES:
		df_materiais = pd.DataFrame({})
		df_licitacoes = pd.DataFrame({})
		df_lotes = pd.DataFrame({})
		tabela_unica = pd.DataFrame({})

		## SCRIPT


		#cria as colunas nos dataframes:
		ChargeGroup2Handler.create_column(df_licitacoes,'Licitações')
		ChargeGroup2Handler.create_column(df_licitacoes,'Lotes')

		ChargeGroup2Handler.create_column(df_lotes,'Licitações')
		ChargeGroup2Handler.create_column(df_lotes,'Lotes')


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

		lote = ChargeGroup2Handler.read_excel('{}/{}/{}'.format(path, df_licitacoes.Licitações[0], df_licitacoes.Infos[0]))
		info = ChargeGroup2Handler.read_excel('{}/{}/{}/{}'.format(path, df_lotes.Licitações[0], 'Lotes', df_lotes.Lotes[0])) 

		ChargeGroup2Handler.create_column(tabela_unica,'pdf_url')
		ChargeGroup2Handler.create_column(tabela_unica,'classificacao')
		ChargeGroup2Handler.create_column(tabela_unica,'fiscal')
		ChargeGroup2Handler.create_column(tabela_unica,'valor_total')
		ChargeGroup2Handler.create_column(tabela_unica,'numero_processo')
		ChargeGroup2Handler.create_column(tabela_unica,'edital')
		ChargeGroup2Handler.create_column(tabela_unica,'objeto')
		ChargeGroup2Handler.create_column(tabela_unica,'contrato')
		ChargeGroup2Handler.create_column(tabela_unica,'materiais_e_servicos')
		ChargeGroup2Handler.create_column(tabela_unica,'demandante')
		ChargeGroup2Handler.create_column(tabela_unica,'empresas')

		ChargeGroup2Handler.create_column(df_materiais,'especificacoes')
		ChargeGroup2Handler.create_column(df_materiais,'quantidade')
		ChargeGroup2Handler.create_column(df_materiais,'valor_unitario')
		ChargeGroup2Handler.create_column(df_materiais,'item')
		ChargeGroup2Handler.create_column(df_materiais,'fornecedor')
		ChargeGroup2Handler.create_column(df_materiais,'unidade')
		ChargeGroup2Handler.create_column(df_materiais,'filename')
	

		### ABRE CADA LOTE DO FORMATO EXCEL E COPIA AS LINHAS DO LOTE PARA A TABELA UNICA
		
		for i in range(len(df_licitacoes)):
			if df_licitacoes.Licitações[i] in list(tabela_unica.numero_processo):
				continue
			lote = yield ChargeGroup2Handler.read_excel('{}/{}/{}'.format(path, df_licitacoes.Licitações[i], df_licitacoes.Infos[i]))

			for k in range(len(lote.index)):
				tabela_unica = tabela_unica.append({'pdf_url': None, 'classificacao': 'ATAS COM VIGÊNCIA EXPIRADA', 'fiscal': lote.pregoeiro[k], 'valor_total': 'R$ {}'.format(lote.ValorArrematado[k]), 'numero_processo':df_licitacoes.Licitações[i],'edital':lote.edital[k], 'objeto':lote.Descricao[k], 'contrato': None, 'materiais_e_servicos': 'SRP 632/2016', 'demandante': 'DISER', 'empresas': [{'valor_estimado': 'R$ {}'.format(lote.ValorUnitário[k]), 'nome_empresa': lote.Nome_Fantasia[k], 'termo_aditivo': None, 'vigencia': lote.vigencia[k], 'valor_global': 'R$ {}'.format(lote.ValorArrematado[k]), 'ata': None, 'descricao_empresa': lote.Atividade_Economica[k]}]}, ignore_index=True)
				info = yield ChargeGroup2Handler.read_excel('{}/{}/{}/{}'.format(path, df_licitacoes.Licitações[i], 'Lotes', arr_infos[i][k])) 
				for j in range(len(info.index)):
						df_materiais = df_materiais.append({'especificacoes': info.Descrição[j], 'quantidade': info.Quantidade[j], 'valor_unitario': lote.ValorUnitário[k], 'item': info.Item[j], 'fornecedor': lote.Nome_Fantasia[k], 'unidade': None, 'numero_processo':df_licitacoes.Licitações[i]}, ignore_index=True)
				
		records2 = json.loads(df_materiais.T.to_json()).values()
		self.application.mongodb.materials.insert(records2)
		#print(tabela_unica)

		groups = tabela_unica.groupby("numero_processo")
		for processo, group in groups:
			arr_empresas = []
			for index, row in group.iterrows():
				#rint(x)
				arr_empresas.append(row['empresas'][0])

			# Finalizada 1 licitacao
			bidding = {'instituicao':"Barreiras-BA",'pdf_url': None, 'classificacao': 'ATAS COM VIGÊNCIA EXPIRADA', 'fiscal': group['fiscal'].iloc[0], 'valor_total': group['valor_total'].iloc[0], 'numero_processo':group['numero_processo'].iloc[0],'edital':group['edital'].iloc[0], 'objeto':group['objeto'].iloc[0], 'contrato': None, 'materiais_e_servicos': None, 'demandante': None, 'empresas': arr_empresas};
			self.application.mongodb.licitacoes.insert(bidding)			


		response = {"status": "function done"}
		self.set_status(200) #http 200 ok
		self.write(response)
		self.finish()
		return
