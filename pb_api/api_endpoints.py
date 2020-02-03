"""
Routes and views for the flask application.
"""

from datetime import datetime
import pkg_resources
from sys import version_info
from flask import jsonify
from pb_api import app

@app.route('/', methods=['GET'])
@app.route('/version', methods=['GET'])
def version():
    return jsonify({
        "pip_version": "{}".format(pkg_resources.get_distribution('pip').version),
        "openSSL_version": "{}".format(pkg_resources.get_distribution('pyopenssl').version),
        "jinja_version": "{}".format(pkg_resources.get_distribution('jinja2').version),
        "mySql_version": "{}".format(pkg_resources.get_distribution('flask-mysql').version),
        "flask_version": "{}".format(pkg_resources.get_distribution('flask').version),
        "python_version": "{}.{}".format(version_info.major, version_info.minor)
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