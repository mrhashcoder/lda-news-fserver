from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
import os
from bson import json_util
import json


@jwt_required()
def user():
    try:
        current_user = get_jwt_identity()
        # print(current_user)
        # Mongo Connection
        mongoURI = os.getenv('MONGO_URI')
        client  = MongoClient(mongoURI)
        db = client.newsDB
        userCollection = db.users       

        user_data = userCollection.find_one({"username" : current_user})
        
        # for json serialization remove object id
        user_data = json.loads(json_util.dumps(user_data))
        
        return jsonify({
            "status" : 200,
            "message" : "Success",
            "user_data" : user_data
        }) , 200
    
    except:
        return jsonify( {
           "status" : 500,
           "message" : "Internal Server Error" 
        } ) , 500
        