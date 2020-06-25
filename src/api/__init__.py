"""
The flask application package.
"""

from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, origins="*", supports_credentials=True)
# Disable sorting of the jsonified data
app.config['JSON_SORT_KEYS'] = False

from api.models import db
import api.models
import api.endpoints
import api.views
import api.utils
