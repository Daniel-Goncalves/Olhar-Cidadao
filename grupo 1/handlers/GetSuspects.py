#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, json, time, re
import pymongo
from pymongo import MongoClient
from InitScrapy import InitScrapy

class Validation():
  def __init__(self):
    # Deleta o arquivo de resultados já obtidos:
    if os.path.isfile('results.json'):
      os.remove("results.json")

    # Conexão com o banco de dados e início do processo de validação de dados:
    self.client = MongoClient('localhost')
    self.import_from_db()
    
  def import_from_db(self):
    # Importação dos dados dos materiais das licitações:
    db = self.client.projeto2
    materials = db.materials

    # Para cada material do BD:
    for material in materials.find():
      # Se a unidade não for 'Hora' (o que significa que é um serviço, fora do escopo do projeto):
      if material['unidade'] != 'Hora':
        # Este produto será validado:
        self.validate_product(material)

  def validate_product(self, product):
    # A descrição do produto, o preço unitário e o nome do fornecedor são extraídos:
    product_name = product['especificacoes']
    suspect_price = product['valor_unitario']
    suspect_company = product['fornecedor']

    # O objeto da classe Scrapy é criado com os dados do produto. Será considerado um máximo de 40 caracteres.
    # A função get_data() buscará preços na internet e retornará o resultado no arquivo results.json:
    InitScrapy(product_name[:40])

    # Listas de resultados e de preços:
    results = []
    prices = []

    # Criação de flag para indicar corrupção:
    flag_corruption = False
    
    # Tratamento do preço do produto para float:
    suspect_price_temp = re.sub("[^0-9,]", "", suspect_price)
    suspect_price_float = float(suspect_price_temp.replace(',','.'))

    # O arquivo results.json é aberto e cada linha é um dicionário.
    # Popula-se a lista de preços já convertidos em float.
    # Popula-se a lista de resultados com vários dicionários:
    with open('results.json') as file:
      for line in file.readlines():
        data = json.loads(line)
        price_temp = re.sub("[^0-9,]", "", data['price'])
        price_float = float(price_temp.replace(',','.'))
        prices.append(price_float)
        results.append(data)

    # Deleta o arquivo de resultados já obtidos:
    os.remove("results.json")

    # Se o valor máximo da lista de preços for menor que o preço na licitação, é uma suspeita de corrupção:
    if max(prices) < suspect_price_float:
      flag_corruption = True

    # Se a flag de corrupção estiver setada como verdadeira:
    if flag_corruption:
      # Um dicionário com a data atual e os dados do produto suspeito são armazenados num dicionário:
      suspect_data = { "date" : time.strftime("%x"), "suspect_product" : product_name, "suspect_price" : price, "suspect_company" : suspect_company }

      # O dicionário criado acima será mesclado com cada dicionário da lista de resultados:
      for result in results:
        result.update(suspect_data)

      print "CORRUPÇÃO!"

      # Os dados serão inseridos numa nova collection do BD:
      # Conexão com o BD é feita:
      db = self.client.projeto2
      collection = db.data_teste
      collection.insert(results)

validation = Validation()