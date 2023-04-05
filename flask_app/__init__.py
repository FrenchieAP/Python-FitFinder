from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh"
DATABASE = "fit_finder_schema"

from flask_app.controllers import users_controller
import logging
logging.basicConfig(level=logging.DEBUG)
