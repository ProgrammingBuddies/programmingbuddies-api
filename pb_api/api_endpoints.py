"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import jsonify
from pb_api import app

@app.route('/', methods=['GET'])
@app.route('/version', methods=['GET'])
def version():
    return jsonify({
        "api_version": "",
        "flask_version": ""
    })

@app.route('/users')
def users():
    return jsonify({
        "1001": "John Smith",
        "1002": "Jane Smith"
    })



@app.route('/projects')
def projects():
    return jsonify({
        "0001": "Community Project #1",
        "0002": "Private Project #1"
    })