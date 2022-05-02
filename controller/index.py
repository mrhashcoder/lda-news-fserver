from flask import jsonify





def index():
    return jsonify({
        "status" : 200,
        "message" : "Success"
    }) , 200