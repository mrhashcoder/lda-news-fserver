from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
import os
import json


@jwt_required()
def like_news():
    try:
        current_user = get_jwt_identity()
        body = request.get_json()
        news_id = body['news_id']
        print(current_user)
        print(news_id)
        
        #mongoDB connection
        mongoURI = os.getenv('MONGO_URI')
        client  = MongoClient(mongoURI)
        db = client.newsDB  
        newsTagCollection = db.newsTagCollection
        userCollection = db.users
        
        news_tags_object = newsTagCollection.find_one({"news_id" : ObjectId(news_id)})
        
        if news_tags_object:
            tags = news_tags_object['tags']    
            print(tags)
            # inserting in liked_news_array
            userCollection.update_many({"username" : current_user} , {'$addToSet' : {"liked_news" : news_id}})

            # inserting in liked_tags_array    
            userCollection.update_many({"username" : current_user} , {'$push' : {'liked_tags' : tags}})

            return jsonify({
                "status" : 200,
                "message" : "success"
            }), 200
        else:
            return jsonify({
                "status" : 400,
                "message" : "incorrect news_id"
            }) , 400
    except:
        return jsonify({
            "status" : 500,
            "message" : "failed"
        }),500


  
def get_news_by_id(id):
    try:     
        # news_object of id   
        objInstance = ObjectId(id) 
        
        # mongoDB connection
        mongoURI = os.getenv('MONGO_URI')
        client  = MongoClient(mongoURI)
        db = client.newsDB  
        newsCollection = db.newsCollection
        
        current_news = newsCollection.find_one({'_id' : objInstance}) 
        
        if current_news:
            current_news = json.loads(json_util.dumps(current_news))
            
            return current_news
        else:
            return {}
            
        
    except Exception:
        return {}
    