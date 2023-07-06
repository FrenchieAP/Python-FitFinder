from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re, requests
# from dotenv import load_dotenv
import os

# load_dotenv()

# GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
# print(f"Google API Key: {GOOGLE_API_KEY}")

class Gym:
    def __init__( self , data ):
        # self.id = data['id']
        self.name = data['name']
        self.formatted_address = data['formatted_address']
        self.photos = data['photos']
        self.rating = data['rating']
        # self.url = data['url']
        # self.photo_reference = data['photo_reference']
        self.place_id = data['place_id']

    @classmethod
    def get_results(cls, find, near):
        query = f"{find} {near}"
        r = requests.get(f"https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyBQMOQnqqPr_QUac8uC00J1ueX5jV3YjMc&query={query}&type=gym")
        result = r.json()
        gym_list = []
        print(result)
        for gym in result["results"]:
            gym_info = {
                "name": gym["name"],
                "formatted_address": gym["formatted_address"],
                "photos" : "No photos",
                "rating" : gym["rating"],
                # "url" : gym["url"],
                "place_id": gym["place_id"]
            }
            try: 
                gym_info["photos"] = f'https://maps.googleapis.com/maps/api/place/photo?photoreference={gym["photos"][0]["photo_reference"]}&sensor=false&maxheight=200&maxwidth=300&key=AIzaSyBQMOQnqqPr_QUac8uC00J1ueX5jV3YjMc'

            except: 
                gym_info["photos"] = "https://i.imgur.com/NO25iZV.png"
            # print(gym_info["photos"])
            this_gym = cls(gym_info)
            gym_list.append(this_gym)
        return gym_list
    
    @classmethod
    def get_by_place_id(cls, place_id):
        r = requests.get(f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key=AIzaSyBQMOQnqqPr_QUac8uC00J1ueX5jV3YjMc")
        result = r.json()
        gym_info = {
            "name": result["result"]["name"],
            "formatted_address": result["result"]["formatted_address"],
            "photos" : "No photos",
            "rating" : result["result"].get("rating"), 
            #The get method of dictionaries returns None if the key is not present in the dictionary, so if the rating key is not present in the response, the value of gym_info["rating"] will be None.
            # "url" : result["result"]["url"],
            "place_id": result["result"]["place_id"]
        }
        try: 
            gym_info["photos"] = f'https://maps.googleapis.com/maps/api/place/photo?photoreference={result["result"]["photos"][0]["photo_reference"]}&sensor=false&maxheight=200&maxwidth=300&key=AIzaSyBQMOQnqqPr_QUac8uC00J1ueX5jV3YjMc'

        except: 
            gym_info["photos"] = "https://i.imgur.com/NO25iZV.png"
        this_gym = cls(gym_info)
        return this_gym





            # @classmethod 
    # def searching(cls, find, near):
    #     query = f"{find} {near}"
    #     r = requests.get(f"https://maps.googleapis.com/maps/api/place/textsearch/json?key={GOOGLE_API_KEY}&query={query}&type=gym")
    #     result = r.json()
    #     print(result)
