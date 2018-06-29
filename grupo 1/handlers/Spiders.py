
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy

# Classe de spider do Scrapy para buscar resultados no Buscapé:
class BuscapeSpider(scrapy.Spider):
  name = 'buscape'

  def __init__(self, product_name):
    self.product_name = product_name
    search_product = '-'.join(product_name.lower().split())
    self.allowed_domains = ['buscape.com.br']
    self.start_urls = ['https://www.buscape.com.br/search/%s' % search_product]


  def parse(self, response):
    product = response.css('div.card--product__name.u-truncate-multiple-line::text').extract()
    price = response.css('span[itemprop=lowPrice]::text').extract()
    store = response.css('strong.bui-product__store::text').extract()

    for item in zip(product, price, store):
      yield {
        'product' : item[0],
        'price' : item[1],
        'store' : item[2],
        'origin' : self.name
      }


# Classe de spider do Scrapy para buscar resultados no Zoom:
class ZoomSpider(scrapy.Spider):
  name = 'zoom'

  def __init__(self, product_name):
    self.product_name = product_name
    search_product = '-'.join(self.product_name.lower().split())
    self.allowed_domains = ['zoom.com.br']
    self.start_urls = ['https://www.zoom.com.br/search?q=%s#produtos' % search_product]

  def parse(self, response):
    product = response.css('div.info-container > p > span::text').extract()
    price = response.css('div.price-container > span:first-of-type::text').extract()
    store = response.css('img[alt*="Comprar em"]::attr(alt)').extract()

    for item in zip(product, price, store):
      yield {
        'product' : item[0],
        'price' : item[1],
        'store' : item[2][11:],
        'origin' : self.name
      }

