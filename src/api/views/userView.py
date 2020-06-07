from flask import request, jsonify, session, Flask, redirect, session, url_for
from flask_login import login_user, login_required, logout_user, current_user
from api import app
from datetime import timedelta
from api.controllers import userController
from os import environ
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer import oauth_authorized

print("hello")
app.secret_key = environ.get("APP_SECRET")
github_blueprint = make_github_blueprint(
    client_id = environ.get("GITHUB_ID"),
    client_secret = environ.get("GITHUB_SECRET")
)

app.register_blueprint(github_blueprint, url_prefix="/login")

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
    app.permanent_session_lifetime = timedelta(seconds=300)

@app.route("/login", methods=["GET"])
def login_route():
    account = request.args.get('account')
    session['action'] = "login"
    session['redirect'] = request.args.get('redirect')

    if account == 'github':
        return redirect(url_for("github.login"))
    else:
        return "", 400

@app.route("/register", methods=["GET"])
def register_route():
    account = request.args.get('account')
    session['action'] = "register"
    session['username'] = request.args.get('username')
    session['redirect'] = request.args.get('redirect')

    if account == 'github':
        return redirect(url_for("github.login"))
    else:
        return "", 400

@oauth_authorized.connect
def oathed(blueprint, token):
    if session['action'] == 'login':
        return login(blueprint)
    elif session['action'] == 'register':
        return register(blueprint)
    else:
        return "", 501

@app.route("/users/sign-out")
@login_required
def sign_out():
    logout_user()
    return "", 200

def login(blueprint):
    if blueprint.name == "github":
        resp = github.get("/user").json()
        id = resp["id"]
        user = userController.get_user(github_id=id)
        if user:
            login_user(user)
        return redirect(session['redirect'])

def register(blueprint):
    if blueprint.name == "github":
        resp = github.get("/user").json()
        id = resp["id"]
        user = userController.get_user(github_id=id)
        if not user:
            user = userController.create_user(github_id=id, name=session["username"])
            login_user(user)
        return redirect(session['redirect'])
