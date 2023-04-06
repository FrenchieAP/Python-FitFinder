from flask import Flask
from config import connectToMySQL

app = Flask(__name__)
app.secret_key = "shhhhhh"
DATABASE = "heroku_1310f620a16f672"
mysql = connectToMySQL(DATABASE)

from flask_app.controllers import users_controller
import logging
logging.basicConfig(level=logging.DEBUG)
