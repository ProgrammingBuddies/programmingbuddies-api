
""" All configration included here """

from os import environ
from sys import argv
from flask_swagger_ui import get_swaggerui_blueprint
from api import app
from secrets import token_urlsafe
from flask_dance.contrib.github import make_github_blueprint

# Keep configurations during development
DEBUG = True

# if DEBUG:
    # develop config
# else:
    # productaion config

""" Documentation """

# swagger specific
SWAGGER_URL = '/docs'
API_URL = '/spec'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': "Programing Buddies API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
# end swagger specific

""" Authentication """

# github oauth
app.secret_key = environ.get("APP_SECRET")
github_blueprint = make_github_blueprint(
    client_id = environ.get("GITHUB_ID"),
    client_secret = environ.get("GITHUB_SECRET")
)

app.register_blueprint(github_blueprint, url_prefix="/login")
app.config['JWT_SECRET_KEY'] = environ.get("JWT_SECRET_KEY")
# end github oauth

""" Database """

# Check CONNECT
db_url = environ.get("CONNECT")
if db_url is None or db_url=="":
    raise ValueError("Environment Variable 'CONNECT' has to be set in the .env file")

# Check if it's sqlite
if db_url == 'sqlite':
    db_url = 'sqlite:///db.sqlite3'

app.config["SQLALCHEMY_DATABASE_URI"] = db_url

from api.models import init_db
if '--reset-db' in argv:
    init_db(True)
else:
    init_db()

""" CORS and other configurations """

# Disable sorting of the jsonified data
app.config['JSON_SORT_KEYS'] = False

""" Old testing data """

"""
# Test data
import datetime;

user1 = User(name='Foe Joe')
user2 = User(name='Tommy Frich')
user3 = User(name='Limm Carter')
link1 = UserLink(name='GitHub', url='https://github.com')
user1.links.append(link1)

project1 = Project(name='Hello, World!', repository="https://github.com/ProgrammingBuddies/programmingbuddies-api", description='First project.', development_status=2, creation_date=datetime.datetime.now())
link2 = ProjectLink(name='Reddit', url='https://reddit.com')
project1.links.append(link2)

userHasProject = UserHasProject(role=1)
userHasProject.project = project1

user1.projects.append(userHasProject)

feedback1 = ProjectFeedback(rating=3, description="Cool project!", project_feed_author=user1, project=project1)
feedback2 = ProjectFeedback(rating=1, description="Not so cool!",  project_feed_author=user2, project=project1)

# project1.feedbacks.append(feedback1)
# project1.feedbacks.append(feedback2)

feedback3 = UserFeedback(user_feed_author=user1, destination=user2, rating=5, description="Good guy!")
feedback4 = UserFeedback(user_feed_author=user3, destination=user2, rating=1, description="Poor guy!")

db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()
"""
