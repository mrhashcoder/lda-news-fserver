from flask import request, jsonify
import os
from numpy import identity
from pymongo import MongoClient
from flask_jwt_extended import create_access_token


def login():
    user = request.get_json()
    
    if(validate_request(user)):
            
        # MongoDB Connection
        mongoURI = os.getenv('MONGO_URI')
        client  = MongoClient(mongoURI)
        db = client.newsDB
        userCollection = db.users       
        
        # Check if User is Correct
        user_exists = userCollection.find_one({"$and" : [{'username' : user['username']} , {'password' : user['password']}]})
        
        if user_exists:
            jwt_token = create_access_token(identity=user['username'])
            return jsonify({
                "status" : 200,
                "message" : "User Logged",
                "jwt_token" : jwt_token
            }) , 200
        
        else:
            return jsonify({
                "status" : "200",
                "message" : "Invalid username or password"
            }) , 200
        
    else:
        return jsonify({
            "status" : 400,
            "message" : "Bad Request",
        }), 400
    
    
    

def validate_request(user):
    try:
        if(user["username"] == None or user["username"].strip() == ""):
            return False
        
        if(user["password"] == None or user["password"].strip() == ""):
            return False
        
        return True
    except:
        return False    