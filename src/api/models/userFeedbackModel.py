from api.models import db
from api.models.column import Column


class UserFeedback(db.Model):
    id = Column(db.Integer, primary_key=True, readonly=True)
    author_id = Column(db.Integer, db.ForeignKey('user.id'), readonly=True)
    user_id = Column(db.Integer, db.ForeignKey('user.id'))
    rating = Column(db.Integer, nullable=False)
    description = Column(db.String(255), nullable=True)

    def as_dict(self):
        obj_d = {
            'id': self.id,
            'author_id': self.author_id,
            'user_id': self.user_id,
            'rating': self.rating,
            'description': self.description,
        }
        return obj_d
