from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re, requests
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Favorite:
    def __init__( self , data ):
        self.id = data['id']
        self.users_id = data['users_id']
        self.name = data['name']
        self.place_id = data['place_id']
