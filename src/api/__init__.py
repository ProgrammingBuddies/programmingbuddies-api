"""
The flask application package.
"""

from flask import Flask
from flask_marshmallow import Marshmallow
app = Flask(__name__)
ma = Marshmallow(app)

from api.models import db
import api.models
import api.endpoints
import api.views
