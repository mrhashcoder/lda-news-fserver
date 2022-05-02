from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
from flask import jsonify, request
from bson import json_util
import os
import json


@jwt_required()
def recommand_news():
    current_user = get_jwt_identity()
    body = request.get_json()
    
    if validate_request(body) == False:
        return jsonify({
            "status" : "400",
            "message" : "Bad request",
        })
    
    page = body["page"]
    page_limit = body["limit"]
    
    # mongoConnection
    try:
        mongoURI = os.getenv('MONGO_URI')
        client  = MongoClient(mongoURI)
        db = client.newsDB
        userCollection = db.users    
        tagCollection = db.tagCollection   
        newsCollection = db.newsCollection
        
        current_user_object = userCollection.find_one({"username" : current_user})
        tags = current_user_object["liked_tags"]
        if(len(tags) == 0):
            return jsonify({
                "status" : 200,
                "news_list" : [],
                "message" : "user don't have any liked news yet"
            }), 200

        news_id_list = []
        for tag_list in tags:
            for tag in tag_list:
                current_tag_object = tagCollection.find_one({'name' : tag})
                news_id_list.extend(current_tag_object['articles'])

        news_id_list = list(set(news_id_list))
        
        fetch_news = newsCollection.find({"_id" : {"$in" : news_id_list}}).sort('_id' , -1).skip(page_limit * (page-1)).limit(page_limit)
        news_fetched = list(json.loads(json_util.dumps(fetch_news)))
        
        return jsonify({
            "status" : 200,
            "news_list" : news_fetched,
            "total_recommanded" : len(news_id_list),
            "page" : page,
            "page_limit" : page_limit,
        })

    except Exception:
        return jsonify({
            "status" : 500,
            "message" : "Server error"
        }), 500
        
        
        
        
def validate_request(body):
    try:
        if(int(body['limit']) <= 0):
            return False

        if(int(body['page']) <= 0):
            return False

        return True
    
    except:
        return False
        