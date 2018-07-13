import tornado.web
from tornado_cors import CorsMixin
from handlers.ConfigHandler import ConfigHandler

class CorsHandler(CorsMixin, tornado.web.RequestHandler):
	
	# Value for the Access-Control-Allow-Origin header.
	# Default: None (no header).
	CORS_ORIGIN = '*'
	
	# Value for the Access-Control-Allow-Headers header.
	# Default: None (no header).
	CORS_HEADERS = 'Content-Type'
	
	# Value for the Access-Control-Allow-Methods header.
	# Default: Methods defined in handler class.
	# None means no header.
	# CORS_METHODS = 'GET'
	# Default methods:
	#  ['get', 'put', 'post', 'patch', 'delete', 'options']
	

	# Value for the Access-Control-Allow-Credentials header.
	# Default: None (no header).
	# None means no header.
	CORS_CREDENTIALS = False
	
	# Value for the Access-Control-Max-Age header.
	# Default: 86400.
	# None means no header.
	CORS_MAX_AGE = 21600

	# Value for the Access-Control-Expose-Headers header.
	# Default: None
	CORS_EXPOSE_HEADERS = 'Location, X-WP-TotalPages'