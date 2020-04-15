from flask import request, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user
from api import app
from datetime import timedelta
from api.controllers import userController

@app.route("/users", methods=['POST'])
def create_user():
    user = userController.create_user(**request.get_json())

    return jsonify(user.as_dict()), 201

@app.route("/users/<id>", methods=['POST'])
@login_required
def update_user(id):
    if 'id' in request.get_json():
        return "", 501
    user = userController.update_user(id, **request.get_json())

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
@login_required
def delete_user(id):
    if int(current_user.id) == int(id):
        user = userController.delete_user(id)

        if user:
            return "", 200
        else:
            return "", 404
    else:
        return "You cannot delete an other user", 401

@app.before_request
def before_sign_in():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=20)

@app.route("/users/sign-in/<name>", methods=["POST"])
def sign_in(name):
    user = userController.get_user(name=name)
    if user == None:
        return "", 400
    else:
        login_user(user)
        return str(user.id), 200

@app.route("/users/sign-out")
@login_required
def sign_out():
    logout_user()
    return "", 200