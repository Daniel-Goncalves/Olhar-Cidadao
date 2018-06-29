import tornado.web
from tornado import gen
import logging
import sys
import re
from datetime import datetime
from collections import namedtuple

from handlers.ConfigHandler import ConfigHandler
from handlers.CorsHandler import CorsHandler


class CompaniesHandler(CorsHandler):


	@gen.coroutine
	def get(self):

		winner_companies = yield CompaniesHandler.get_winner_companies_as_list(self)
		companies_that_won_in_multiple_biddings = yield CompaniesHandler.get_company_winning_in_all_biddings(self)
		companies_that_won_in_multiple_biddings_with_high_value = yield CompaniesHandler.get_company_winning_in_all_biddings_above_value_threshold(self)
		companies_that_won_in_the_same_bidding = yield CompaniesHandler.get_company_winning_in_same_bidding(self)
		companies_that_won_in_the_same_bidding_with_high_value = yield CompaniesHandler.get_company_winning_in_same_bidding_above_value_threshold(self)
		companies_vigent_ranges = yield CompaniesHandler.get_companies_vigent_ranges(self)
		companies_that_won_in_same_period = yield CompaniesHandler.company_winning_more_than_one_bidding_in_the_same_period(self)
		companies_that_won_multiple_times_considering_total_values = yield CompaniesHandler.get_company_winning_considering_company_size(self)

		CompaniesHandler.save_suspectious(self,companies_that_won_in_multiple_biddings,companies_that_won_in_multiple_biddings_with_high_value,companies_that_won_in_the_same_bidding,companies_that_won_in_the_same_bidding_with_high_value,companies_that_won_in_same_period,companies_that_won_multiple_times_considering_total_values)

		response = {
			'Winner companies': winner_companies,
			'Companies that won multiple times in all bidding':companies_that_won_in_multiple_biddings,
			'Companies that won in multiple biddings with high value':companies_that_won_in_multiple_biddings_with_high_value,
			'Companies that won multiple times in the same bidding':companies_that_won_in_the_same_bidding,
			'Companies that won multiple times in the same bidding with high value':companies_that_won_in_the_same_bidding_with_high_value,
			'Companies that won multiple times in the same period':companies_that_won_in_same_period,
			'Companies that won multiple times considering company size':companies_that_won_multiple_times_considering_total_values
		}
		self.set_status(200)  # http 200 ok
		self.write(response)
		self.finish()
		return


	@gen.coroutine
	def get_winner_companies(self):
		cursor = self.application.mongodb.licitacoes.find({"classificacao":"ATAS COM VIGÊNCIA EXPIRADA"})
		winner_companies = {}
		while (yield cursor.fetch_next):

			element = cursor.next_object()
			companies = element['empresas']
			licit = element['objeto']

			for company in companies:
				# Company has already won any process
				if company['nome_empresa'] in winner_companies:
					winner_companies[company['nome_empresa']]['number_of_wins'] += 1
					winner_companies[company['nome_empresa']]['total_value'] += CompaniesHandler.convert_one_value(company['valor_global'])
					winner_companies[company['nome_empresa']]['wonBiddings'].append(licit)
				else:
					winner_companies[company['nome_empresa']] = {"number_of_wins":1,"total_value":CompaniesHandler.convert_one_value(company['valor_global']),"wonBiddings":[licit]}

		return winner_companies

	@gen.coroutine
	def get_winner_companies_as_list(self):
		cursor = self.application.mongodb.licitacoes.find({"classificacao":"ATAS COM VIGÊNCIA EXPIRADA"})
		winner_companies = {}
		while (yield cursor.fetch_next):

			element = cursor.next_object()
			companies = element['empresas']
			licit = element['objeto']

			for company in companies:
				# Company has already won any process
				if company['nome_empresa'] in winner_companies:
					winner_companies[company['nome_empresa']]['number_of_wins'] += 1
					winner_companies[company['nome_empresa']]['total_value'] += CompaniesHandler.convert_one_value(company['valor_global'])
					winner_companies[company['nome_empresa']]['wonBiddings'].append(licit)
				else:
					winner_companies[company['nome_empresa']] = {"number_of_wins":1,"total_value":CompaniesHandler.convert_one_value(company['valor_global']),"wonBiddings":[licit]}
		
		winner_companies_array = []
		for key in winner_companies:
			winner_companies_array.append({"nome_empresa":key,"number_of_wins":winner_companies[key]['number_of_wins'],"total_value":winner_companies[key]['total_value'],"wonBiddings":winner_companies[key]['wonBiddings']})


		return winner_companies_array

	@gen.coroutine
	def get_company_winning_in_all_biddings(self):
		winner_companies = yield CompaniesHandler.get_winner_companies(self)
		for key,value in list(winner_companies.items() ):
			if value['number_of_wins'] <= ConfigHandler.maximum_number_of_wins_for_a_company_in_all_biddings:
				del winner_companies[key]
		return winner_companies

	@gen.coroutine
	def get_company_winning_in_all_biddings_above_value_threshold(self):
		winner_companies = yield CompaniesHandler.get_winner_companies(self)
		for key,value in list(winner_companies.items() ):
			if value['number_of_wins'] <= ConfigHandler.maximum_number_of_wins_for_a_company_in_all_biddings or CompaniesHandler.convert_one_value(value['total_value']) <= ConfigHandler.maximum_total_value_allowed:
				del winner_companies[key]
		return winner_companies

	@gen.coroutine
	def get_company_winning_considering_company_size(self):
		winner_companies = yield CompaniesHandler.get_winner_companies(self)

		#winner_companies['Ferragens Lider Comercio e Serviços EIRELI - EPP']['number_of_wins'] = 2

		for key,value in list(winner_companies.items() ):
			if value['number_of_wins'] == 1:
				#nothing = 1
				del winner_companies[key]
			elif value['number_of_wins'] == 2 and CompaniesHandler.convert_one_value(value['total_value']) <= ConfigHandler.maximum_value_allowed_for_two_wins:
				del winner_companies[key]
			elif value['number_of_wins'] == 3 and CompaniesHandler.convert_one_value(value['total_value']) <= ConfigHandler.maximum_value_allowed_for_three_wins:
				del winner_companies[key]

		return winner_companies

	@gen.coroutine
	def get_company_winning_in_same_bidding(self):

		cursor = self.application.mongodb.licitacoes.find({"classificacao":"ATAS COM VIGÊNCIA EXPIRADA"})
		winner_companies = []
		while (yield cursor.fetch_next):
			element = cursor.next_object()
			companies = element['empresas']

			aux_dict = {"licitacao":element['objeto'],'multiple_win_companies':{}}
			for company in companies:
				if company['nome_empresa'] in aux_dict['multiple_win_companies']:
					aux_dict['multiple_win_companies'][company['nome_empresa']]['number_of_win'] += 1
					aux_dict['multiple_win_companies'][company['nome_empresa']]['valor_total'] += company['valor_global']
				else:
					aux_dict['multiple_win_companies'][company['nome_empresa']] = {'valor_total':company['valor_global'],'number_of_win':1}

			aux_dict = CompaniesHandler.convert_valor_total_to_number(aux_dict)

			# Remove those who have won less than 2
			for key,value in list(aux_dict['multiple_win_companies'].items() ):
				if value['number_of_win'] <= ConfigHandler.maximum_number_of_wins_same_bidding:
					del aux_dict['multiple_win_companies'][key]

			if len(aux_dict['multiple_win_companies']) > 0:
				winner_companies.append(aux_dict)	
		
		return winner_companies

	def convert_valor_total_to_number(dict):
		for key,value in list(dict['multiple_win_companies'].items() ):
			valor_total =  value['valor_total']
				
			converted_value = CompaniesHandler.convert_one_value(valor_total)

			dict['multiple_win_companies'][key]['valor_total'] = converted_value
		return dict

	def convert_one_value(value):
		value = str(value)
		aux_value = re.sub("[^0-9,]", "", value)
		converted_value = float(aux_value.replace(",","."))
		return converted_value

	@gen.coroutine
	def get_company_winning_in_same_bidding_above_value_threshold(self):
		winner_companies = yield CompaniesHandler.get_company_winning_in_same_bidding(self)

		for element in winner_companies:
			for key,value in list(element['multiple_win_companies'].items() ):
				valor_total =  value['valor_total']
				if valor_total <= ConfigHandler.maximum_total_value_allowed:
					del element['multiple_win_companies'][key]

		for element in winner_companies[:]:
			if len(element['multiple_win_companies']) == 0:
				winner_companies.remove(element)

		return winner_companies

	@gen.coroutine
	def get_companies_vigent_ranges(self):

		cursor = self.application.mongodb.licitacoes.find({"classificacao":"ATAS COM VIGÊNCIA EXPIRADA"})
		dateranges = {}
		Range = namedtuple('Range', ['start', 'end'])
		while (yield cursor.fetch_next):

			element = cursor.next_object()
			companies = element['empresas']
			licitacao = element['objeto']
			numero_processo = element['numero_processo']

			for company in companies:
				# Company has already won any process
				date = company['vigencia']
				start = date.split("-")[0][:-1].split("/")
				end = date.split("-")[1][1:].split("/")
				date_range = Range(start=str(datetime(int(start[2]), int(start[1]), int(start[0]) ) ), end=str(datetime(int(end[2]), int(end[1]), int(end[0]) )))

				json = {"licitacao":licitacao,"daterange":date_range,"numero_processo":numero_processo}

				if company['nome_empresa'] in dateranges:
					dateranges[company['nome_empresa']].append(json)
				else:
					dateranges[company['nome_empresa']] = [json]

		return dateranges

	@gen.coroutine
	def company_winning_more_than_one_bidding_in_the_same_period(self):
		date_ranges = yield CompaniesHandler.get_companies_vigent_ranges(self)
		# At this point i have the dateranges for each company
		# Now it's necessary to check if any date overlaps

		
		#Range = namedtuple('Range', ['start', 'end'])
		#r1 = Range(start=str(datetime(2016, 6, 30)), end=str(datetime(2016, 7, 6)))
		#json = {"licitacao":"SERVIÇO DE INTALAÇÃO DE FORROS","daterange":r1 }
		#date_ranges['José Espedito Cavalcanti - ME'].append(json)
		
		overlaping_dates = []

		for key in date_ranges:
			# List of dateranges for a company
			for i in range(0,len(date_ranges[key])):
				licit1 = date_ranges[key][i]['licitacao']
				numero_processo1 = date_ranges[key][i]['numero_processo']
				range1 = date_ranges[key][i]['daterange']
				for j in range(i+1,len(date_ranges[key])):
					licit2 =  date_ranges[key][j]['licitacao']
					numero_processo2 = date_ranges[key][j]['numero_processo']
					range2 = date_ranges[key][j]['daterange']
					overlaped_days = CompaniesHandler.dates_overlap_days(range1,range2)
					if overlaped_days != 0:
						overlaping_dates.append({"company":key,"Licitacao1":{"nome":licit1,"numero_processo":numero_processo1,"Range":range1},"Licitacao2":{"nome":licit2,"numero_processo":numero_processo2,"Range":range2},"Overlaped days":overlaped_days})

		return overlaping_dates


	def dates_overlap_days(r1,r2):			# Return the number of days two date ranges overlap

		#r1 = Range(start=datetime(2015, 01, 01), end=datetime(2015, 01, 01))
		latest_start=max(datetime.strptime(r1[0],"%Y-%m-%d %H:%M:%S"),datetime.strptime(r2[0],"%Y-%m-%d %H:%M:%S"))
		earliest_end=min(datetime.strptime(r1[1],"%Y-%m-%d %H:%M:%S"),datetime.strptime(r2[1],"%Y-%m-%d %H:%M:%S"))
		delta=(earliest_end-latest_start).days

		if delta>0:
			return delta+1
		else:
			return 0

	def save_suspectious(self,companies_that_won_in_multiple_biddings,companies_that_won_in_multiple_biddings_with_high_value,companies_that_won_in_the_same_bidding,companies_that_won_in_the_same_bidding_with_high_value,companies_that_won_in_same_period,companies_that_won_multiple_times_considering_total_values):
		# Save erros in db		
		# Remove all previous errors, once all the biddings will be analyzed
		self.application.mongodb.suspicious_biddings.remove()
		for key in companies_that_won_in_multiple_biddings:
			self.application.mongodb.suspicious_biddings.insert({"suspected":"Company won multiple biddings","company":key,"wins":companies_that_won_in_multiple_biddings[key]})
		for key in companies_that_won_in_multiple_biddings_with_high_value:
			self.application.mongodb.suspicious_biddings.insert({"suspected":"Company won multiple biddings in a high value","company":key,"wins":companies_that_won_in_multiple_biddings_with_high_value[key]})
		for element in companies_that_won_in_the_same_bidding:
			for key in element['multiple_win_companies']:
				self.application.mongodb.suspicious_biddings.insert({"suspected":"Company won multiple times in the same bidding","company":key,"wins":element['multiple_win_companies'][key]})
		for element in companies_that_won_in_the_same_bidding_with_high_value:
			for key in element['multiple_win_companies']:
				self.application.mongodb.suspicious_biddings.insert({"suspected":"Company won multiple times in the same bidding with high value","company":key,"wins":element['multiple_win_companies'][key]})
		for element in companies_that_won_in_same_period:
			self.application.mongodb.suspicious_biddings.insert({"suspected":"Company won multiple in the same period","company":key,"wins":element})
		for key in companies_that_won_multiple_times_considering_total_values:
			self.application.mongodb.suspicious_biddings.insert({"suspected":"Company won multiple times considering company size","company":key,"wins":companies_that_won_multiple_times_considering_total_values[key]})
