from api.models import db, User

class UserController:
    session = db.session()
    def create_user(self, **kwargs):
        user = User(**kwargs)
        self.session.add(user)
        self.session.commit()

    def get_user(self, **kwargs):
        user = User.query.filter_by(**kwargs).first()
        return user

userController = UserController()
