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
    Returns versions of all dependencies
    ---
    tags:
        - Info
    responses:
        200:
            description: List of versions of dependencies
    """
    return jsonify({
        "python_version": "{}.{}".format(version_info.major, version_info.minor),
        "pip_version": "{}".format(pkg_resources.get_distribution('pip').version),
        "flask-dance_version": "{}".format(pkg_resources.get_distribution('flask-dance').version),
        "oauthlib_version": "{}".format(pkg_resources.get_distribution('oauthlib').version),
        "requests_version": "{}".format(pkg_resources.get_distribution('requests').version),
        "certifi_version": "{}".format(pkg_resources.get_distribution('certifi').version),
        "cherdet_version": "{}".format(pkg_resources.get_distribution('chardet').version),
        "idna_version": "{}".format(pkg_resources.get_distribution('idna').version),
        "urllib3_version": "{}".format(pkg_resources.get_distribution('urllib3').version),
        "urlobject_version": "{}".format(pkg_resources.get_distribution('urlobject').version),
        "pyopenssl_version": "{}".format(pkg_resources.get_distribution('pyopenssl').version),
        "flask-sqlalchemy_version": "{}".format(pkg_resources.get_distribution('flask-sqlalchemy').version),
        "sqlalchemy_version": "{}".format(pkg_resources.get_distribution('sqlalchemy').version),
        "sqlalchemy-utils_version": "{}".format(pkg_resources.get_distribution('sqlalchemy-utils').version),
        "flask-swagger_version": "{}".format(pkg_resources.get_distribution('flask-swagger').version),
        "pyyaml_version": "{}".format(pkg_resources.get_distribution('pyyaml').version),
        "flask-swagger-ui_version": "{}".format(pkg_resources.get_distribution('flask-swagger-ui').version),
        "jinja2_version": "{}".format(pkg_resources.get_distribution('jinja2').version),
        "flask_version": "{}".format(pkg_resources.get_distribution('flask').version),
        "cffi_version": "{}".format(pkg_resources.get_distribution('cffi').version),
        "pycparser_version": "{}".format(pkg_resources.get_distribution('pycparser').version),
        "click_version": "{}".format(pkg_resources.get_distribution('click').version),
        "cryptography_version": "{}".format(pkg_resources.get_distribution('cryptography').version),
        "itsdangerous_version": "{}".format(pkg_resources.get_distribution('itsdangerous').version),
        "jsonify_version": "{}".format(pkg_resources.get_distribution('jsonify').version),
        "mysql-connector-python_version": "{}".format(pkg_resources.get_distribution('mysql-connector-python').version),
        "protobuf_version": "{}".format(pkg_resources.get_distribution('protobuf').version),
        "setuptools_version": "{}".format(pkg_resources.get_distribution('setuptools').version),
        "markupsafe_version": "{}".format(pkg_resources.get_distribution('markupsafe').version),
        "pycparser_version": "{}".format(pkg_resources.get_distribution('pycparser').version),
        "six_version": "{}".format(pkg_resources.get_distribution('six').version),
        "werkzeug_version": "{}".format(pkg_resources.get_distribution('werkzeug').version)
    })

@app.route("/spec")
def spec():
    """
        API spec
        Return the swagger api specification.
        ---
        tags:
            - Docs
        responses:
            200:
                description: API spec documentation
        """
    swag = swagger(app)

    swag['swagger'] = '2.0'

    swag['info']['version'] = '1.0'
    swag['info']['title'] = 'Programming Buddies API'
    swag['info']['description'] = 'Projects\' management system'

    swag['info']['license'] = {'name': 'GPL 3.0', 'url': 'https://opensource.org/licenses/GPL-3.0'}

    return jsonify(swag)
