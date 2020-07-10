from api.controllers.validationController import validateForCreate, validateForUpdate
from api.models import db, User, UserHasProject, UserLink, UserFeedback
from api.validation.UserValidation import UserLinkCreateValidation, UserLinkUpdateValidation, UserFeedbackCreateValidation, UserUpdateValidation
from flask_jwt_extended import get_jwt_identity


class UserController:
    session = db.session()

    # User
    def create_user(self, **kwargs):
        try:
            if not kwargs.get("name", False):
                return None, "Missing required argument", 400
            else:
                user = User(**kwargs)
                self.session.add(user)
                self.session.commit()

            return user, "OK", 200
        except:
            self.session.rollback()
            return None, "Forbidden Attributes", 400

    def update_user(self, user_id, req):
        try:
            v = validateForUpdate(req, UserUpdateValidation, User)
            if v == True:
                user = User.query.filter_by(id=user_id).first()
                if user is None:
                    return None, "user not found", 404

                json = req.get_json()
                for key, value in json.items():
                    setattr(user, key, value)

                db.session.commit()

                return user, "OK", 200
            else:
                return v
        except Exception as e:
            print(type(e))
            print(e)
            self.session.rollback()
            return None, "user update failed", 500

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
    def create_link(self, user_id, req):
        try:
            v = validateForCreate(req, UserLinkCreateValidation, UserLink)
            if v == True:
                json = req.get_json()
                user = User.query.filter_by(id=user_id).first()
                if user is None:
                    return None, "User not found", 404

                link = UserLink(user_id=user_id, **json)
                self.session.add(link)
                self.session.commit()

                return link, "OK", 201
            else:
                return v

        except Exception as e:
            print(type(e))
            print(e)
            self.session.rollback()
            return None, "link creation failed", 500

    def update_link(self, user_id, req):
        try:
            v = validateForUpdate(req, UserLinkUpdateValidation, UserLink)
            if v == True:
                json = req.get_json()
                link = UserLink.query.filter_by(user_id=user_id, id=json['id']).first()

                if link is None:
                    return None, "User doesn't have a link with that id or user doesn't exist", 404

                for key, value in json.items():
                    setattr(link, key, value)

                self.session.commit()
                return link, "OK", 200
            else:
                return v

        except Exception as e:
            print(type(e))
            print(e)
            self.session.rollback()
            return None, "link update failed", 500

    def get_all_links(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return None, "User not found", 404

        return [link for link in user.links], "OK", 200

    def delete_link(self, user_id, req):
        try:
            link = UserLink.query.filter_by(user_id=user_id, id=req.args.get('id')).first()

            if link is None:
                return None, "Link not found", 404

            db.session.delete(link)
            db.session.commit()

            return link, "OK", 200

        except Exception as e:
            print(type(e))
            print(e)
            self.session.rollback()
            return None, "link deletion failed", 500

    # User Feedback
    def create_feedback(self, user_id, req):
        try:
            v = validateForCreate(req, UserFeedbackCreateValidation, UserFeedback)
            if v == True:
                author = User.query.filter_by(id=user_id).first()
                if author is None:
                    return None, "Author not found", 404

                json = req.get_json()
                user = User.query.filter_by(id=json['user_id']).first()
                if user is None:
                    return None, "User not found", 404

                feedback = UserFeedback(author_id=author.id, **json)
                self.session.add(feedback)
                self.session.commit()

                return feedback, "OK", 201
            else:
                return v

        except Exception as e:
            print(type(e))
            print(e)
            self.session.rollback()
            return None, "feedback creation failed", 500

    def get_all_feedbacks(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return None, "User not found", 404

        return [feedback for feedback in user.received_feedbacks], "OK", 200

    def delete_feedback(self, user_id, req):
        user = User.query.filter_by(id=user_id).first()
        if user == None:
            return None, "User not found", 404

        feedback = UserFeedback.query.filter_by(author_id=user_id, id=req.args.get("id")).first()
        if feedback == None:
            return None, "feedback not found", 404

        db.session.delete(feedback)
        db.session.commit()

        return feedback, "OK", 200

    def get_user_from_jwt(self):
        return self.get_user(id=get_jwt_identity())


userController = UserController()
