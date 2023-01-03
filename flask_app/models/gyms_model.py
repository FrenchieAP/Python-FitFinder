from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re, requests

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

    # @classmethod 
    # def searching(cls, find, near):
    #     query = f"{find} {near}"
    #     r = requests.get(f"https://maps.googleapis.com/maps/api/place/textsearch/json?key=ApiKeyGoesHere&query={query}&type=gym")
    #     result = r.json()
    #     print(result)

    @classmethod
    def get_results(cls, find, near):
        query = f"{find} {near}"
        r = requests.get(f"https://maps.googleapis.com/maps/api/place/textsearch/json?key=ApiKeyGoesHere&query={query}&type=gym")
        result = r.json()
        gym_list = []
        print(result)
        for gym in result["results"]:
            gym_info = {
                "name": gym["name"],
                "formatted_address": gym["formatted_address"],
                "photos" : "No photos",
                "rating" : gym["rating"],
                # "url" : gym["url"]
                "place_id": gym["place_id"]
            }
            try: 
                gym_info["photos"] = f'https://maps.googleapis.com/maps/api/place/photo?photoreference={gym["photos"][0]["photo_reference"]}&sensor=false&maxheight=200&maxwidth=300&key=ApiKeyGoesHere'

            except: 
                gym_info["photos"] = "https://i.imgur.com/NO25iZV.png"
            # print(gym_info["photos"])
            this_gym = cls(gym_info)
            gym_list.append(this_gym)
        return gym_list
