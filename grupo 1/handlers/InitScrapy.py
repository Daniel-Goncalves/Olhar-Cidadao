
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from handlers.Spiders import BuscapeSpider, ZoomSpider
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process, Queue


# Classe do Scrapy para iniciar o processo de scraping e construir o arquivo JSON com os resultados:
class InitScrapy():

	def crawl(Spider,product_name):
		def f(q):
			try:
				runner = CrawlerRunner({
				'FEED_FORMAT': 'jsonlines',
				'FEED_URI': 'results.json'
				})
				process = runner.crawl(Spider,product_name)
				process.addBoth(lambda _: reactor.stop())
				reactor.run()
				q.put(None)
			except Exception as e:
				q.put(e)

		q = Queue()
		p = Process(target=f, args=(q,))
		p.start()
		result = q.get()
		p.join()

		if result is not None:
			raise result

	# A função get_data() buscará preços na internet e retornará o resultado no arquivo results.json:
	#@defer.inlineCallbacks
	def get_data(product_name):

		#yield process.crawl(BuscapeSpider, product_name)
		#yield process.crawl(ZoomSpider, product_name)
		#process.start()]
		#reactor.stop()

		InitScrapy.crawl(BuscapeSpider,product_name)
		InitScrapy.crawl(ZoomSpider,product_name)

