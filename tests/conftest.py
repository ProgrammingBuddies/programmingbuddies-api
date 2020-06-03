import pytest
from sqlalchemy_utils import database_exists, create_database
from os import environ
from tests import app, db

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
