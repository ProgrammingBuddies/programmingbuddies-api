"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

from api.models import db
import api.models
import api.endpoints
