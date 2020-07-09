
"""

  Creates valid model objects for testing purposes:

    - insert data to the database which could be used for testing

    - these functions will give back the created objects in dict format which is hardcoded at every model's as_dict instance method

    - call these functions form any test case.

"""
from flask_jwt_extended import create_access_token
from tests import db, Project, User, UserHasProject, UserLink, ProjectLink, UserFeedback

""" Create relationship between user and project """
def user_join_project_for_test_cases(user, project):
    userHasProject = UserHasProject(role=1)
    userHasProject.project = Project.query.filter_by(id=project["id"]).first()
    userHasProject.user = user
    # This line is not needed for some reason
    # SQLAlchemy is doing some magic and I don't know shit about fuck
    #user.projects.append(userHasProject)
    db.session.commit()

def create_project_for_test_cases(data):
    new_project = Project(**data)
    db.session.add(new_project)
    db.session.commit()

    return new_project.as_dict()

def delete_user_for_test_cases(user):
    db.session.delete(user)
    db.session.commit()

def create_project_link_for_test_cases(data):
    new_project_link = ProjectLink(**data)
    db.session.add(new_project_link)
    db.session.commit()

    return new_project_link.as_dict()

def create_access_token_for_test_cases(data):
    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return create_access_token(identity=new_user), new_user

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

def create_user_feedback_for_test_cases(user1, user2):
    feedback_data = {
        "author_id": user1["id"],
        "user_id": user2["id"],
        "description": "This is the description",
        "rating": 1
    }

    new_user_feedback = UserFeedback(**feedback_data)
    db.session.add(new_user_feedback)
    db.session.commit()

    return new_user_feedback.as_dict()
