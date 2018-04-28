import base64
import logging
import tornado.web
from tornado import gen
import json
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

from handlers.ConfigHandler import ConfigHandler

class ChargeUnbBiddings(tornado.web.RequestHandler):

    @gen.coroutine
    def get_html_table(self):
        # Get html code to match pdf urls after create dataframe
        html = requests.get(self.unb_biddings_url).content
        soup = BeautifulSoup.BeautifulSoup(html)
        table = soup.find("table")
        html_table = BeautifulSoup.BeautifulSoup(str(table))
        return html_table

    @gen.coroutine
    def create_licit_df(self):
        #self.table = pd.read_html(unb_biddings_url)[0]
        #columns = table.iloc[2].tolist()   # This row actually represents the columns. Pop 0 because the first element is the row number
        #columns.pop(0)
        columns = ['objeto','numero_processo','materiais_e_servicos','contrato','empresas','edital','demandante','fiscal','valor_total','classificacao','pdf_url']
        licit_df = pd.DataFrame(columns=columns)
        return licit_df


    @gen.coroutine
    def find_pdf_url(self,identifier):
        for tr in self.html_table.findAll("tr"):
            trs = tr.findAll("td")
            if len(trs) > 0:
                if len(trs) > 1 and trs[2].text == identifier:
                    try:
                        return trs[2].a["href"]
                    except:     # Row does not have a pdf url
                        return

    @gen.coroutine
    def update_unb_biddings(self):
        #records = licit_df.to_json(orient='records')
        records = json.loads(self.licit_df.T.to_json()).values()
        for record in records:
            self.licit_collection.update({'numero_processo':record['numero_processo']},record,upsert=True)

    @gen.coroutine
    def treat_table_row(self,row_info,state,index_row):
        objeto=numero_processo=materiais_e_servicos=ata=nome_empresa=edital=vigencia=valor_global=valor_estimado=demandante=fiscal=contrato= None

        if self.table.iloc[index_row].notnull().sum() == 1:
            # Linha em branco -> Fim de ATAS COM VIGÊNCIA EXPIRADA
            self.inicio_proxima_classificacao = index_row + 3
            return False
        elif self.new_object:

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
            self.empresas.append({"ata":ata,"termo_aditivo":termo_aditivo,"nome_empresa":nome_empresa,"vigencia":vigencia,"valor_global":valor_global,"valor_estimado":valor_estimado})

            self.new_object = False
        elif self.table.iloc[index_row].notnull().sum() == 6:        # Outra empresa no mesmo objeto

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
            self.empresas.append({"ata":ata,"termo_aditivo":termo_aditivo,"nome_empresa":nome_empresa,"vigencia":vigencia,"valor_global":valor_global,"valor_estimado":valor_estimado})

        elif row_info[0] == "Valor Total:": 
            # Concluido um objeto
            valor_total = row_info[1]
            self.licit_df.loc[self.licit_df_index] = [objeto,numero_processo,materiais_e_servicos,contrato,self.empresas,edital,demandante,fiscal,valor_total,state,None]
            self.licit_df_index = self.licit_df_index + 1
            self.new_object = True
            self.empresas = []   
        return True

    @gen.coroutine
    def post(self):

        self.unb_biddings_url = ConfigHandler.unb_biddings_url
        self.html_table = self.get_html_table()
        self.licit_df = yield self.create_licit_df()

        self.licit_collection = self.application.mongodb.licitacoes     
        self.table = pd.read_html(self.unb_biddings_url)[0]
        self.inicio_proxima_classificacao = 0 

        post_data = tornado.escape.json_decode(self.request.body)

        #user = post_data["account"]    

        self.licit_df_index = 0
        self.empresas = []
        self.new_object = True
        collection = self.application.mongodb.licitacoes

        #cursor = yield collection.find_one(query_object)
        #result = bool(cursor)        # True se encontrado usuario

       
        state = "ATAS COM VIGÊNCIA EXPIRADA"
        for index_row in range(3,len(self.table)):
            row_info = self.table.iloc[index_row].tolist()
            row_info.pop(0)                             # First element is the index, so remove it
            if(not self.treat_table_row(row_info,state,index_row)):    # When it returns false, it's next state
                break
            
        empresas = []
        self.new_object = True
        state = "CONTRATOS EXPIRADOS"
        for index_row in range(self.inicio_proxima_classificacao,len(self.table)):
            row_info = self.table.iloc[index_row].tolist()

            row_info.pop(0)
            if(not self.treat_table_row(row_info,state,index_row)):
                break

        # Assign pdf urls
        for i,(index, row) in enumerate(self.licit_df.iterrows()):

            if getattr(row, "classificacao") == "ATAS COM VIGÊNCIA EXPIRADA":
                identifier = getattr(row, "materiais_e_servicos")
            if getattr(row, "classificacao") == "CONTRATOS EXPIRADOS":
                identifier = getattr(row, "contrato")

            pdf_url = self.find_pdf_url(identifier)
            self.licit_df.loc[index]['pdf_url'] = pdf_url

        self.update_unb_biddings()

        response = {
            'status': 'ok',
            'msg': 'unb biddings updated in database'
        }
        self.set_status(200)  # http 200 ok
        self.write(response)
        self.finish()
        return

        
