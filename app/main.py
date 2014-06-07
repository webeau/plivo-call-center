from config import app_config
from routes import route_list
from services.db_helper import DBHelper
import webapp2

db_helper = DBHelper()
app = webapp2.WSGIApplication(route_list,
                              config=app_config,
                              debug=app_config.get('debug', False))