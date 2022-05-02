from dotenv import load_dotenv
from flask import request, jsonify
import os
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
import json
    

def news_pagination():
    data = request.get_json()
    page = int(data['page'])
    page_limit = int(data['limit'])
    
    if validate_request(data):
        # mongoDB connection
        mongoURI = os.getenv('MONGO_URI')
        client  = MongoClient(mongoURI)
        db = client.newsDB  
        newsCollection = db.newsCollection
        
        news_count = newsCollection.count_documents({})
        fetch_news = newsCollection.find().sort('_id' , -1).skip(page_limit * (page-1)).limit(page_limit)
        news_fetched = list(json.loads(json_util.dumps(fetch_news)))
        
        return jsonify({
            "status" : 200,
            "message" : "ok",
            "total_news" : news_count,
            "news_list" : news_fetched
        }),200
    else:    
        return jsonify({
            "status": 400,
            "message": "Bad Request",
        }), 400
    

def news_by_id(id):    
    try:        
        objInstance = ObjectId(id) 
        
        load_dotenv()
        mongoURI = os.getenv('MONGO_URI')
        client  = MongoClient(mongoURI)
        db = client.newsDB  
        newsCollection = db.newsCollection
        
        current_news = newsCollection.find_one({'_id' : objInstance}) 
        
        if current_news:
            current_news = json.loads(json_util.dumps(current_news))
            
            return jsonify({
                "status": 200,
                "message": "ok",
                "news": current_news
            })
            pass
        else:
            return jsonify({
                "status": "400",
                "message": "News Not Found"
            }),400
            
        
    except Exception:
        return jsonify({
            "status": 400,
            "message": "Bad Request",
        }), 400
    
    
    
def validate_request(body):
    try:
        if(int(body['limit']) <= 0):
            return False

        if(int(body['page']) <= 0):
            return False

        return True
    
    except:
        return False
