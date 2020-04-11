"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
# Disable sorting of the jsonified data
app.config['JSON_SORT_KEYS'] = False

from api.models import db
import api.models
import api.endpoints
import api.views
