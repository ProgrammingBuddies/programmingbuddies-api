import os
import sys

# todo: change this importing solution
sys.path.insert(0, os.getcwd()+'/src')

from api import app
from api.models import db
from api.models import User, Project, UserFeedback, ProjectFeedback, UserLink, ProjectLink

sys.path.insert(0, os.getcwd()+'/tests')
