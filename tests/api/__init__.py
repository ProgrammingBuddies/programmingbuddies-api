
"""

  Creates valid model objects for testing purposes:

    - insert data to the database which could be used for testing

    - these functions will give back the created objects in dict format which is hardcoded at every model's as_dict instance method

    - call these functions form any test case.

"""

from tests import db, Project, User, UserLink, ProjectLink

def create_project_for_test_cases(data):
    new_project = Project(**data)
    db.session.add(new_project)
    db.session.commit()
    return new_project.as_dict()

def create_project_link_for_test_cases(data):
    new_project_link = ProjectLink(**data)
    db.session.add(new_project_link)
    db.session.commit()
    return new_project_link.as_dict()

def create_user_for_test_cases(data):
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return new_user.as_dict()

def create_user_link_for_test_cases(data):
    new_user_link = UserLink(**data)
    db.session.add(new_user_link)
    db.session.commit()
    return new_user_link.as_dict()
