from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh"
DATABASE = "fit_finder_schema"