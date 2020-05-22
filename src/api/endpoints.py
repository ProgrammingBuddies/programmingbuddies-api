"""
Routes and views for the flask application.
"""

import pkg_resources
import os
from flask import send_from_directory
from sys import version_info
from flask import jsonify
from flask_swagger import swagger
from api import app

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/', methods=['GET'])
@app.route('/version', methods=['GET'])
def version():
    """
    Get server's dependencies versions
    ---
    responses:
        200:
            description: Everything went alright
    """
    return jsonify({
        "pip_version": "{}".format(pkg_resources.get_distribution('pip').version),
        "pyopenssl_version": "{}".format(pkg_resources.get_distribution('pyopenssl').version),
        "jinja2_version": "{}".format(pkg_resources.get_distribution('jinja2').version),
        "flask_version": "{}".format(pkg_resources.get_distribution('flask').version),
        "cffi_version": "{}".format(pkg_resources.get_distribution('cffi').version),	
        "click_version": "{}".format(pkg_resources.get_distribution('click').version),
        "cryptography_version": "{}".format(pkg_resources.get_distribution('cryptography').version),
        "itsdangerous_version": "{}".format(pkg_resources.get_distribution('itsdangerous').version),
        "jsonify_version": "{}".format(pkg_resources.get_distribution('jsonify').version),
        "markupsafe_version": "{}".format(pkg_resources.get_distribution('markupsafe').version),
        "pycparser_version": "{}".format(pkg_resources.get_distribution('pycparser').version),
        "six_version": "{}".format(pkg_resources.get_distribution('six').version),
        "werkzeug_version": "{}".format(pkg_resources.get_distribution('werkzeug').version),
        "python_version": "{}.{}".format(version_info.major, version_info.minor)
    })

@app.route("/swagger_spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Programming Buddies API"
    return jsonify(swag)
