from flask import request, jsonify
from api import app
from api.controllers import userController
from api.models.userModel import UserSchema

userSchema = UserSchema()
usersSchema = UserSchema(many=True)

@app.route("/users", methods=['POST'])
def post_user():
    user = userController.create_user(**request.get_json())

    return jsonify(userSchema.dump(user)), 201

@app.route("/users/<id>", methods=['GET'])
def get_user(id):
    user = userController.get_user(id=id)

    if user:
        return jsonify(userSchema.dump(user)), 200
    else:
        return "", 404

@app.route("/users", methods=['GET'])
def get_all_users():
    all_users = userController.get_all_users()

    return jsonify(usersSchema.dump(all_users)), 200

@app.route("/users/<id>", methods=['DELETE'])
def delete_user(id):
    result = userController.delete_user(id)

    if result:
        return "", 202
    else:
        return "", 404