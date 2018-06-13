#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import logging
import sys, os, json, time, re
import pymongo
from pymongo import MongoClient
from UnbScrapy import UnbScrapy

class Validation():
  def __init__(self):
    # Deleta o arquivo de resultados já obtidos:
    if os.path.isfile('results.json'):
      os.remove("results.json")

    self.validate_products()
    

  def validate_products(self):
    # Dados fixos, essa parte ficara dentro de um for para pegar todos os produtos do BD:
    product_name = 'Alicate Para Eletrodo (500 A)'
    suspect_price = '552,90'
    suspect_company = "ANTONIO LIMITADA"

    # O objeto da classe Scrapy é criado com os dados do produto. Será considerado um máximo de 30 caracteres.
    # A função get_data() buscará preços na internet e retornará o resultado no arquivo results.json:
    UnbScrapy(product_name[:30], suspect_price).get_data()

    # Lista de resultados e de preços, flag para indicar corrupção e o preço do produto em float:
    results = []
    prices = []
    flag_corruption = False
    suspect_price_temp = re.sub("[^0-9,]", "", suspect_price)
    suspect_price_float = float(price_temp.replace(',','.'))

    # O arquivo results.json é aberto e cada linha é um dicionário.
    # Popula-se a lista de preços já convertidos em float.
    # Popula-se a lista de resultados com vários dicionários:
    with open('results.json') as file:
      for line in file.readlines():
        data = json.loads(line)
        prices.append(float(data['price'].replace(',','.')))
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
      print "##########################################################################"
      client = MongoClient('localhost')
      db = client.teste_data
      collection = db.data_teste
      collection.insert(results)
      print "##########################################################################"

validation = Validation()