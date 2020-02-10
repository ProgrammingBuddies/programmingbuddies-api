"""
Routes and views for the flask application.
"""

import pkg_resources
from sys import version_info
from flask import jsonify
from api import app

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
