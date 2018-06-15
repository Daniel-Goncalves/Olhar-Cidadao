'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from Spiders import BuscapeSpider, ZoomSpider

# Classe do Scrapy para iniciar o processo de scraping e construir o arquivo JSON com os resultados:
class UnbScrapy(object):
  def __init__(self, product_name, price):
    self.product_name = product_name
    self.price = price

  def get_data(self):
    process = CrawlerProcess({
      'FEED_FORMAT': 'jsonlines',
      'FEED_URI': 'results.json'
      })
    process.crawl(BuscapeSpider, self.product_name)
    process.crawl(ZoomSpider, self.product_name)
    process.start()
'''
