from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, get_jwt_claims, create_access_token
from api.models import User
from flask import request, jsonify, session, Flask, redirect, session, url_for
from api import app
from os import environ
from api.controllers import userController
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer import oauth_authorized

app.secret_key = environ.get("APP_SECRET")
github_blueprint = make_github_blueprint(
    client_id = environ.get("GITHUB_ID"),
    client_secret = environ.get("GITHUB_SECRET")
)

app.register_blueprint(github_blueprint, url_prefix="/login")

app.config['JWT_SECRET_KEY'] = environ.get("JWT_SECRET_KEY")
# JWT token expiration time in seconds - default is 15 minutes
if environ.get("JWT_ACCESS_TOKEN_EXPIRES"):
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = environ.get("JWT_ACCESS_TOKEN_EXPIRES")
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@app.route("/login", methods=["GET"])
def login_route():
    account = request.args.get('account')
    session['action'] = "login"
    session['redirect'] = request.args.get('redirect')
    session['state'] = request.args.get('state','{}')

    if account == 'github':
        return redirect(url_for("github.login"))
    else:
        return "", 400

@app.route("/register", methods=["GET"])
def register_route():
    account = request.args.get('account')
    session['action'] = "register"
    # TODO remove or not?
    session['username'] = request.args.get('username')
    session['redirect'] = request.args.get('redirect')
    session['state'] = request.args.get('state','{}')

    if account == 'github':
        return redirect(url_for("github.login"))
    else:
        return "", 400

@oauth_authorized.connect
def oathed(blueprint, token):
    if session['action'] == 'login':
        return login_callback(blueprint)
    elif session['action'] == 'register':
        return register_callback(blueprint)
    else:
        return "", 501


def login_callback(blueprint):
    if blueprint.name == "github":
        resp = github.get("/user").json()
        id = resp["id"]
        user, msg, code = userController.get_user(github_id=id)
        redirect_token = f"?state={session.pop('state', '{}')}"
        if user:
            access_token = create_access_token(identity=user)
            redirect_token += f"&token={access_token}"
        else:
            redirect_token += f"&msg={msg}&code={code}"

        return redirect(session.pop("redirect") + redirect_token)

def register_callback(blueprint):
    if blueprint.name == "github":
        resp = github.get("/user").json()
        id = resp["id"]
        user, msg, code = userController.get_user(github_id=id)
        redirect_token = f"?state={session.pop('state')}"
        if user is None:
            user, msg, code = userController.create_user(github_id=id, name=session.pop('username', "Anton"))

        if user is None:
            redirect_token += f"&msg={msg}&code={code}"
        else:
            access_token = create_access_token(identity=user)
            redirect_token += f"&token={access_token}"

        return redirect(session.pop('redirect') + redirect_token)

