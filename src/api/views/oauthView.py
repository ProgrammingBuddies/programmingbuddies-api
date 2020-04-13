from api import app 
from requests_oauthlib import OAuth2Session
from flask import Flask, request, redirect, session, url_for
from api.controllers import userController

client_id = ""
client_secret = ""
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


@app.route("/auth")
def auth():
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route("/callback", methods=["GET"])
def callback():
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret, authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))

@app.route("/profile", methods=["GET"])
def profile():
    github = OAuth2Session(client_id, token=session['oauth_token'])
    user = github.get('https://api.github.com/user').json()
    username = user['login']
    email = user['email']

    if(userController.get_user(username=username) == None):
        if(email != None):
            userController.create_user(username=username, email=email)
"""
        else:
            #---GITHUB ACCOUNT HAS NO PUBLIC EMAIL ADDRESS---
    
    else:
        #---LOGIN PROCESS?---
"""

    