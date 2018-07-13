import tornado.web
from tornado import gen
import logging
import sys
import re
from datetime import datetime

from handlers.ConfigHandler import ConfigHandler
from handlers.CorsHandler import CorsHandler
from handlers.CompareCompaniesHandler import CompareCompaniesHandler


class CurrentPeriodsHandler(CorsHandler):


	# Return the number of wins separated in months for each institution
	@gen.coroutine
	def post(self):

		post_data = tornado.escape.json_decode(self.request.body)
		institution = post_data['instituicao']

		dates_dict = {}
		cursor = self.application.mongodb.licitacoes.find({"instituicao":institution})
		while (yield cursor.fetch_next):
			element = cursor.next_object()

			for empresa in element['empresas']:
				vigencia = empresa['vigencia']
				start = vigencia.split("-")[0][:-1].split("/")
				start_datetime = str(datetime(int(start[2]), int(start[1]), int(start[0]) ) )
				year_month = start_datetime[:7]

				value = CompareCompaniesHandler.convert_one_value(empresa['valor_global'])
				if year_month in dates_dict:
					dates_dict[year_month]['wins'] += 1
					dates_dict[year_month]['value'] += value
				else:
					dates_dict[year_month] = {"wins":1,"value":value}

		dates_dict = CurrentPeriodsHandler.fulfill_months(dates_dict)
		array = []
		for date in sorted(dates_dict, reverse=True):
			dict = {}
			dict["date"] = date
			dict["wins"] = dates_dict[date]['wins']
			dict["value"] = dates_dict[date]['value']
			array.append(dict)

		self.set_status(200)  # http 200 ok
		self.write({"Dates":array})
		self.finish()
		return


	def fulfill_months(dates_dict):
		sorted_dates = sorted(dates_dict)

		first_date = sorted_dates[0]
		first_year = int(first_date[:4])
		first_month = int(first_date[5:])
		
		last_date = sorted_dates[len(sorted_dates) - 1]
		last_year = int(last_date[:4])
		last_month = int(last_date[5:])

		year_iterations = (last_year - first_year - 1) * 12
		if year_iterations < 0:
			year_iterations = 0
		month_iterations = (12 - first_month) + last_month

		current_year,current_month = first_year,first_month + 1 
		for i in range(0, month_iterations + year_iterations):

			if current_month >= 10:
				year_month = str(current_year) +"-"+str(current_month)
			else:
				year_month = str(current_year) + "-0"+str(current_month)
			if not year_month in dates_dict:
				dates_dict[year_month] = {"wins":0,"value":0}

			current_month += 1
			if(current_month == 13):
				current_month = 1
				current_year += 1

		return dates_dict