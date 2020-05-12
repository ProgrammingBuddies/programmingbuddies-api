from api.models import db, User, UserHasProject, UserLink

class UserController:
    session = db.session()
    def create_user(self, **kwargs):
        try:
            user = User(**kwargs)
            self.session.add(user)
            self.session.commit()

            return user
        except:
            return None
    
    def update_user(self, id, **kwargs):
        user = User.query.filter_by(id=id).first()

        if user == None:
            return None

        for key, value in kwargs.items():
            if key == 'id':
                return None
            elif not hasattr(user, key):
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
            return user
        
        db.session.delete(user)
        db.session.commit()
        
        return user

userController = UserController()
