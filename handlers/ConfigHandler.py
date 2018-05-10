import yaml
import sys
import os

class ConfigHandler:

	# Le arquivo de configuracao
	config_file_stream = open(os.path.join(sys.path[0], "config.yaml"), "r")
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

	config_file_stream.close()
