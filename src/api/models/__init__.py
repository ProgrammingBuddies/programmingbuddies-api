"""
The database package
"""
from sys import argv
from api.models.database import db, init_db
from api.models.userModel import User

if '--reset-db' in argv:
    init_db(True)
else:
    init_db()
