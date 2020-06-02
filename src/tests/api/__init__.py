
"""

  Creates valid model objects for testing purposes:

    - these functions will give back the object's id

    - if you want to access the object properties, then run a query on the model with the given id
      example: User.query.filter_by(id=returned_id)


  -Call these function form any test case.

"""

from tests import db, Project, User, UserLink, ProjectLink

def create_project_for_test_cases(data):
    new_project = Project(**data)
    db.session.add(new_project)
    db.session.commit()
    return new_project.id

def create_user_for_test_cases(data):
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return new_user.id

def create_user_link_for_test_cases(data):
    new_user_link = UserLink(**data)
    db.session.add(new_user)
    db.session.commit()
    return new_user_link.id

def create_project_for_test_cases(data):
    new_project_link = ProjectLink(**data)
    db.session.add(new_project_link)
    db.session.commit()
    return new_project_link.id
