from api import app 
from os import environ
from flask import Flask, request, redirect, session, url_for
from flask_dance.contrib.github import make_github_blueprint, github

print("hello")
app.secret_key = environ.get("APP_SECRET")
github_blueprint = make_github_blueprint(
    client_id = environ.get("GITHUB_ID"),
    client_secret = environ.get("GITHUB_SECRET")
)

app.register_blueprint(github_blueprint, url_prefix="/login")

@app.route("/login/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    uid = resp.json()["id"]
    print(uid)
    return "You are @{login} on GitHub".format(login=resp.json()["login"])