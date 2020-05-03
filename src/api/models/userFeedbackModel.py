from api.models import db
# from api.models.userModel import User

class UserFeedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    author = db.relationship('User', foreign_keys=[author_id], backref='author')
    user = db.relationship('User', foreign_keys=[user_id], backref='user')

    def as_dict(self):
        obj_d = {
            'id': self.id,
            'author': self.author_id,
            'user': self.user_id,
            'rating': self.rating,
            'description': self.description,
        }
        return obj_d
