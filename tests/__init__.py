import os
import sys

# todo: change this importing solution
sys.path.insert(0, os.getcwd()+'/src')

from os import environ
from api import app
from api.models import db
from api.models import User, Project, UserFeedback, ProjectFeedback, UserLink, ProjectLink
from api.models.database import init_db

# Only create database table when testing in the CI.
# When testing in CI, we asume the DB is fresh everytime the
# tests runs, so we *have* to create all models (tables) inside of it.
if environ.get('FLASK_ENV', 'false'):
    init_db(True)

sys.path.insert(0, os.getcwd()+'/tests')
