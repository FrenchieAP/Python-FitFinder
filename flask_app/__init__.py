from flask import Flask
from flask_app.config.mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = "shhhhhh"
# DATABASE = "fit_finder_schema"
DATABASE = "heroku_1310f620a16f672"
mysql = connectToMySQL(DATABASE)

from flask_app.controllers import users_controller
import logging
logging.basicConfig(level=logging.DEBUG)
