import os
from pymongo import MongoClient
from flask import jsonify, request
import json
from bson import json_util

def tag_list():
    try:
        mongoURI = os.getenv('MONGO_URI')
        client  = MongoClient(mongoURI)
        db = client.newsDB
        tagCollection = db.tagCollection  
        
        all_tags = tagCollection.find({})
        print(all_tags)
        tag_list = []
        for tag in all_tags:
            tag_list.append(tag['name'])
        
        return jsonify({
            "status" : 200,
            "message" : "success",
            "tag_list" : tag_list
        })
        
    except Exception:
        return jsonify({
            "status" : 500,
            "message" : "Server Error"
        }), 500

def tag_list_with_count():
    try:
        mongoURI = os.getenv('MONGO_URI')
        client  = MongoClient(mongoURI)
        db = client.newsDB
        tagCollection = db.tagCollection  
        
        all_tags = tagCollection.find({})
        print(all_tags)
        tag_list = []
        for tag in all_tags:
            tag_list.append((tag['name'] ,len(tag['articles']) ))
        
        return jsonify({
            "status" : 200,
            "message" : "success",
            "tag_list" : tag_list
        })
        
    except Exception:
        return jsonify({
            "status" : 500,
            "message" : "Server Error"
        }), 500    

def news_by_tag():
    try:
        body = request.get_json()
        tag_name = body['tag_name']
        print(tag_name)
        if tag_name == '' or tag_name == None:
            return jsonify({
                "status" : 400,
                "message" : "Bad Request"
            }), 400
        
        # mongo Connection
        mongoURI = os.getenv('MONGO_URI')
        client  = MongoClient(mongoURI)
        db = client.newsDB
        tagCollection = db.tagCollection  
        newsCollection = db.newsCollection
        
        tag_object = tagCollection.find_one({"name" : tag_name})
        print(tag_object)
        news_id_list = tag_object['articles']
        
        print(news_id_list)
        
        fetch_news = newsCollection.find({"_id" : {"$in" : news_id_list}})
        news_fetched = list(json.loads(json_util.dumps(fetch_news)))
        
        return jsonify({
            "status" : 200,
            "message" : "success",
            "news_list" : news_fetched,
            "total_news" : len(news_fetched)
        })
        
    except Exception:
        return jsonify({
            "status" : 500,
            "message" : "Server Error"
        }), 500
        