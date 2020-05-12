from flask import request, jsonify
from api import app
from api.controllers import userController

@app.route("/users", methods=['POST'])
def create_user():
    user = userController.create_user(**request.get_json())

    if user == None:
        return "Failed to create user.", 400
    else:
        return jsonify(user.as_dict()), 201

@app.route("/users/<id>", methods=['POST'])
def update_user(id):
    user = userController.update_user(id, **request.get_json())

    if user == None:
        return "Failed to update user.", 400
    else:
        return jsonify(user.as_dict()), 200

@app.route("/users/<id>", methods=['GET'])
def get_user(id):
    user = userController.get_user(id=id)

    if user:
        return jsonify(user.as_dict()), 200
    else:
        return "", 404

@app.route("/users", methods=['GET'])
def get_all_users():
    all_users = userController.get_all_users()

    users = [ user.as_dict() for user in all_users ]

    return jsonify(users), 200

@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    user = userController.delete_user(id)

    if user:
        return "", 200
    else:
        return "", 404