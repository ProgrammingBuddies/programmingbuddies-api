import pytest
from sqlalchemy_utils import database_exists, create_database
from os import environ
from tests import app, db

"""
todo: change this importing solution if the tests/ won't be under src/
import sys
import os
sys.path.insert(0, os.getcwd()+'/src')
import api
sys.path.insert(0, os.getcwd()+'/tests')
"""

@pytest.fixture
def client():

    # delete table entries before each test
    for model in db.Model._decl_class_registry.values():
        try:
            db.session.query(model).delete()
            db.session.commit()
        except:
            pass

    with app.test_client() as test_client:
        yield test_client
