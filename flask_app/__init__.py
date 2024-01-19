from flask import Flask
from flask_app.config.mysqlconnection import connectToMySQL

app = Flask(__name__)
app.secret_key = "shhhhhh"
DATABASE = "defaultdb"
mysql = connectToMySQL(DATABASE)

from flask_app.controllers import users_controller
import logging
logging.basicConfig(level=logging.DEBUG)
