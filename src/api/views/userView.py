from flask import request, jsonify
from api import app
from api.controllers import userController
from api.models.userModel import UserSchema

userSchema = UserSchema()
usersSchema = UserSchema(many=True)

@app.route("/user/push", methods=['POST'])
def push_user():
    user = userController.create_user(**request.form)
    return "200OK"

@app.route("/user/get/<name>", methods=['GET'])
def get_user(name):
    user = userController.get_user(name=name)
    return user.name

@app.route("/users", methods=['GET'])
def get_all_users():
    all_users = userController.get_all_users()

    return jsonify(usersSchema.dump(all_users))