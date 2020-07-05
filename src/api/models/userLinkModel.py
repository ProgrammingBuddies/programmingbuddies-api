from api.models import db
from api.models.column import Column


class UserLink(db.Model):
    id = Column(db.Integer, primary_key=True, readonly=True)
    name = Column(db.String(80), nullable=False)
    url = Column(db.Text, nullable=False)
    user_id = Column(db.Integer, db.ForeignKey('user.id'), nullable=False, readonly=True)

    def as_dict(self):
        obj_d = {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'user_id': self.user_id
        }
        return obj_d

    def __repr__(self):
        return '<UserLink %r>' % self.name
