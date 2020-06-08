from api.models import db, User, UserHasProject, UserLink, UserFeedback

class UserController:
    session = db.session()

    # User
    def create_user(self, **kwargs):
        try:
            user = User(**kwargs)
            self.session.add(user)
            self.session.commit()

            return user
        except:
            self.session.rollback()
            return None

    def update_user(self, id, **kwargs):
        user = User.query.filter_by(id=id).first()

        if user == None:
            return None

        for key, value in kwargs.items():
            if not hasattr(user, key):
                return None

        for key, value in kwargs.items():
            setattr(user, key, value)

        db.session.commit()

        return user

    def get_user(self, **kwargs):
        user = User.query.filter_by(**kwargs).first()

        return user

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
            return None

        db.session.delete(user)
        db.session.commit()

        return user

    # User Link
    def create_link(self, user_id, **kwargs):
        try:
            link = UserLink(user_id=user_id, **kwargs)
            self.session.add(link)
            self.session.commit()

            return link
        except:
            self.session.rollback()
            return None

    def update_link(self, user_id, link_id, **kwargs):
        link = UserLink.query.filter_by(user_id=user_id, id=link_id).first()

        if link == None:
            return None

        for key, value in kwargs.items():
            if not hasattr(link, key):
                return None

        for key, value in kwargs.items():
            setattr(link, key, value)

        db.session.commit()

        return link

    def get_all_links(self, user_id):
        all_links = UserLink.query.filter_by(user_id=user_id).all()

        return all_links

    def delete_link(self, user_id, link_id):
        link = UserLink.query.filter_by(user_id=user_id, id=link_id).first()

        if link == None:
            return None

        db.session.delete(link)
        db.session.commit()

        return link

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

userController = UserController()
