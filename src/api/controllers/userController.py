from api.models import db, User, UserHasProject, UserLink, UserFeedback
from api import app
from flask_jwt_extended import get_jwt_identity
from flask import jsonify

class UserController:
    session = db.session()

    # User
    def create_user(self, **kwargs):
        try:
            user = User(**kwargs)
            self.session.add(user)
            self.session.commit()

            return user, "OK", 200
        except:
            self.session.rollback()
            return None, "Forbidden Attributes", 400

    def update_user(self, id, **kwargs):
        user = User.query.filter_by(id=id).first()

        if user == None:
            return None, "user not found", 404

        for key, value in kwargs.items():
            if not hasattr(user, key):
                return None, "forbidden attribute", 400

        for key, value in kwargs.items():
            setattr(user, key, value)

        db.session.commit()

        return user, "OK", 200

    def get_user(self, **kwargs):
        user = User.query.filter_by(**kwargs).first()

        if user is None:
            return None, "User Not Found", 404

        return user, "OK", 200

    def get_all_users(self, **kwargs):
        all_users = User.query.all()

        return all_users

    def delete_user(self, id):
        # Remove all user's links
        for link in UserLink.query.filter_by(user_id=id).all():
            db.session.delete(link)

        # Remove user from all projects
        for project in UserHasProject.query.filter_by(user_id=id).all():
            db.session.delete(project)

        user = User.query.filter_by(id=id).first()

        if user == None:
            return None, "user not found", 404

        db.session.delete(user)
        db.session.commit()

        return user, "OK", 200
    # User Link
    def create_link(self, user_id, **kwargs):
        try:
            if 'name' in kwargs and 'url' in kwargs and len(kwargs) == 2:
                if kwargs['name'] is None or kwargs['url'] is None:
                    return None, "Arguments can't be empty", 400
                link = UserLink(user_id=user_id, **kwargs)
                self.session.add(link)
                self.session.commit()

                return link, "OK", 201
            else:
                return None, "Forbidden attributes used in request. only name and url allowed.", 400
        except:
            self.session.rollback()
            return None, "link creation failed", 500

    def update_link(self, user_id, **kwargs):
        if not 'id' in kwargs:
            return None, "Missing required parameter 'id'", 400
        print(kwargs['id'])
        print(user_id)
        link = UserLink.query.filter_by(user_id=user_id, id=kwargs['id']).first()

        if link == None:
            return None, "User doesn't have a link with that id or user doesn't exist", 404

        for key, value in kwargs.items():
            if not hasattr(link, key):
                return None, f"Forbidden attribute {key} used", 400

        for key, value in kwargs.items():
            setattr(link, key, value)

        db.session.commit()

        return link, "OK", 200

    def get_all_links(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return None, "User not found", 404
        
        return user.links, "OK", 200

    def delete_link(self, user_id, **kwargs):
        if not 'id' in kwargs:
            return None, "Missing required parameter 'id'", 400

        link = UserLink.query.filter_by(user_id=user_id, id=kwargs['id']).first()

        if link == None:
            return None, "Link not found", 404

        db.session.delete(link)
        db.session.commit()

        return link, "OK", 200

    # User Feedback
    def create_feedback(self, user_id, **kwargs):
        try:
            feedback = UserFeedback(user_id=user_id, **kwargs)
            self.session.add(feedback)
            self.session.commit()

            return feedback
        except:
            self.session.rollback()
            return None

    def get_all_feedbacks(self, user_id):
        all_feedbacks = UserFeedback.query.filter_by(user_id=user_id).all()

        return all_feedbacks

    def delete_feedback(self, user_id, feedback_id):
        feedback = UserFeedback.query.filter_by(user_id=user_id, id=feedback_id).first()

        if feedback == None:
            return None

        db.session.delete(feedback)
        db.session.commit()

        return feedback

    def get_user_from_jwt(self):
        return self.get_user(id=get_jwt_identity())

userController = UserController()
