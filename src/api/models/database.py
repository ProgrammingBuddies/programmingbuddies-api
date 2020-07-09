from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from api import app

db_url = app.config.get("SQLALCHEMY_DATABASE_URI")
db = SQLAlchemy(app)

def init_db(reset=False):
    flag = database_exists(db_url)
    if not flag:
        create_database(db_url)
    if reset:
        db.drop_all()
        db.create_all()
        db.session.commit()
