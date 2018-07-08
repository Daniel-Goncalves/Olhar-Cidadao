import yaml
import sys
import os

class ConfigHandler:

	# Le arquivo de configuracao
	config_file_stream = open(os.path.join(sys.path[0], "config.yaml"), "r",encoding='utf-8')
	config = yaml.load(config_file_stream)


	#mongodb_user = config["database"]["mongodb"]["user"]
	#mongodb_password = config["database"]["mongodb"]["password"]
	mongodb_address = config["database"]["mongodb"]["address"]
	mongodb_db_name = config["database"]["mongodb"]["db_name"]
	mongodb_min_pool_size = config["database"]["mongodb"]["min_pool_size"]

	log_level = config["logging"]["level"]
	log_file = config["logging"]["filename"]

	unb_biddings_url = config['biddings']['unb_biddings_url']
	ocrwebserviceURL = config['biddings']['ocrwebserviceURL']

	item_names_array = config['biddings']['item_names_array']
	qtd_names_array = config['biddings']['qtd_names_array']
	und_names_array = config['biddings']['und_names_array']
	especificacoes_names_array = config['biddings']['especificacoes_names_array']
	valor_unit_names_array = config['biddings']['valor_unit_names_array']
	fornecedor_names_array = config['biddings']['fornecedor_names_array']

	maximum_unit_value = config['treatment']['maximum_unit_value']
	maximum_number_of_wins_same_bidding = config['treatment']['maximum_number_of_wins_same_bidding']
	maximum_total_value_allowed = config['treatment']['maximum_total_value_allowed']
	maximum_number_of_wins_for_a_company_in_all_biddings = config['treatment']['maximum_number_of_wins_for_a_company_in_all_biddings']
	maximum_value_allowed_for_two_wins = config['treatment']['maximum_value_allowed_for_two_wins']
	maximum_value_allowed_for_three_wins = config['treatment']['maximum_value_allowed_for_three_wins']

	config_file_stream.close()
