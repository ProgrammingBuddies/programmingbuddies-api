from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from api import app
from os import environ
db_url = environ.get("CONNECT")
if db_url is None or db_url=="":
    raise ValueError("Environment Variable 'CONNECT' has to be set in the .env file")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url

db = SQLAlchemy(app)
def init_db(reset=False):
    flag = database_exists(db_url)
    if not flag:
        create_database(db_url)
    if reset:
        db.drop_all()
        db.create_all()
        db.session.commit()
