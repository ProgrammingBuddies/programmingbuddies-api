from api import app

from api.controllers import userController
from flask import request

@app.route("/user/push", methods=['POST'])
def push_user():
    user = userController.create_user(**request.form)
    return "200OK"

@app.route("/user/get/<name>", methods=['GET'])
def get_user(name):
    user = userController.get_user(username=name)
    return user.username
