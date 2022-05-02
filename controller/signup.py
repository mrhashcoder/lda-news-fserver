from pymongo import MongoClient
from flask import request, jsonify
import os


def signup():
    try:
        new_user = request.get_json()
        if(validate_request(new_user)):
            # mongoDB Connection
            mongoURI = os.getenv('MONGO_URI')
            client  = MongoClient(mongoURI)
            db = client.newsDB
            userCollection = db.users
            
            
            user_exists = userCollection.find_one({"username" : new_user['username']})
            
            if user_exists is not None:
                return jsonify({
                    "status" : 200,
                    "message" : "User Exists"
                }), 200
            
            # saving new User Object
            user_object = {
                "username" : new_user['username'],
                "password" : new_user['password'],
                "liked_tags" : [],
                "liked_news" : []
            }
            
            userCollection.insert_one(user_object)
            
            return jsonify({
                "status" : 200,
                "message" : "success"
            }), 200
        else:
            return jsonify({
                "status" : 400,
                "message" : "Bad Request"
            }), 400
    except:
        return jsonify({
            "status" : 500,
            "message" : "Internal Server Error"
        }), 500


def validate_request(user):
    try:
        if(user["username"] == None or user["username"].strip() == ""):
            return False
        
        if(user["password"] == None or user["password"].strip() == ""):
            return False
        
        return True
    except:
        return False