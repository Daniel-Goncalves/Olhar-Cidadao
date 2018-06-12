#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from Spiders import BuscapeSpider, ZoomSpider

# Classe do Scrapy para iniciar o processo de scraping e construir o arquivo JSON com os resultados:
class InitScrapy(object):
  def __init__(self, product_name):
    self.product_name = product_name

    self.get_data()

  # A função get_data() buscará preços na internet e retornará o resultado no arquivo results.json:
  def get_data(self):
    process = CrawlerProcess({
      'FEED_FORMAT': 'jsonlines',
      'FEED_URI': 'results.json'
      })
    process.crawl(BuscapeSpider, self.product_name)
    process.crawl(ZoomSpider, self.product_name)
    process.start()