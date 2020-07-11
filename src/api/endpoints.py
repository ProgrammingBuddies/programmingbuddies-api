"""
Routes and views for the flask application.
"""

import os
from sys import version_info

import pkg_resources
from api import app
from flask import jsonify
from flask import send_from_directory
from flask_swagger import swagger


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

    installed_packages = sorted(pkg_resources.working_set, key=lambda x: x.key)
    jsonDict = {"python_version": "{}.{}".format(version_info.major, version_info.minor)}
    for i in installed_packages:
        jsonDict[i.key] = i.version

    return jsonify(jsonDict)


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
