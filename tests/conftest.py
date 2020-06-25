
"""

When the testing process is starting this file will run at first.

This should contain all the neccessary functions for the test flow or at least should be imported here.

"""

import pytest
from sqlalchemy_utils import database_exists, create_database
from os import environ
from tests import app, db

# Provide default test client for testing endpoints
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
        with app.app_context():
            yield test_client
