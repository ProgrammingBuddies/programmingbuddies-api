from api.models import db, User, UserHasProject, UserLink
from flask_login import LoginManager
from api import app

class UserController:
    session = db.session()

    login_manager = LoginManager()
    login_manager.init_app(app)

    def create_user(self, **kwargs):
        user = User(**kwargs)
        self.session.add(user)
        self.session.commit()

        return user
    
    def update_user(self, id, **kwargs):
        user = User.query.filter_by(id=id).first()

        if user == None:
            return user

        for key, value in kwargs.items():
            setattr(user, key, value)

        db.session.commit()

        return user

    @login_manager.user_loader
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
            return user
        
        db.session.delete(user)
        db.session.commit()
        
        return user

userController = UserController()
